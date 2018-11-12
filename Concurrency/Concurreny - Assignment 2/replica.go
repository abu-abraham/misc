package main

import (
	"fmt"
	"strings"
	"time"
)

type Replica struct {
	id Authority

	// blockGenerator is a synchronous read-only channel. It is written to
	// whenever the Replica should generate a Block and propagate it to other
	// Replicas in the network.
	blockGenerator <-chan time.Time

	// blockQueryReceiver is a synchronous read-only channel used to receive
	// Queries that have been sent by other Replicas.
	blockQueryReceiver <-chan Query

	// blockReceiver is a synchronous read-only channel used to receive Blocks
	// that have been sent by other Replicas. Blocks received from this channel
	// are not necessarily to be valid.
	blockReceiver <-chan Blocks

	// conns is an array of connections. It is useful for sending Blocks and
	// BlockQueries to other Replicas in the network. Connections are not
	// guaranteed to be alive, and sending on a dead connection will block
	// forever.
	conns []chan<- Blocks

	blockchains  Blockchains
	authorities  []Authority
	stepDuration int64
}

func NewReplica(id Authority, authorities []Authority, blockReceiver <-chan Blocks, blockQueryReceiver <-chan Query, blockGenerator <-chan time.Time, conns []chan<- Blocks) Replica {
	return Replica{
		id: id,

		blockReceiver:      blockReceiver,
		blockQueryReceiver: blockQueryReceiver,
		blockGenerator:     blockGenerator,

		conns: conns,

		blockchains:  NewBlockchains(),
		authorities:  authorities,
		stepDuration: configStep,
	}
}

// Sign a Block and return it. This marks the Block as being produced by this
// Replica. If the Replica is a not a valid Authority, or the it was not the
// Replicas turn to produce a Block, other Replicas will reject the Block. It is
// assumed that the signing of a Block cannot be forged.
func (replica *Replica) Sign(block Block) Block {
	block.Signature = Signature(string(block.Header) + ":" + string(replica.id))
	return block
}

// IndexOf : To find the index of the authority
func (replica *Replica) IndexOf(id Authority) int {
	for i, v := range replica.authorities {
		if v == id {
			return i
		}
	}
	return -1
}

// IdenfityAuthority : To identify an authority given a timestamp
func IdenfityAuthority(t int64) int {
	q := int(configStep)
	s := int(t) / q
	return s % len(Authorities)
}

// Log : To log in debug mode
func Log(a ...interface{}) {
	debug := false
	if !debug {
		return
	}
	fmt.Println(a)
}

// Send : To send the blocks to the mentioned authority.
// Required to parallaly process when connectivity is low.
func (replica *Replica) Send(newLong Blocks, i int) {
	replica.conns[i] <- newLong
	Log("Completed the sent operation to, ", replica.authorities[i])
}

// SendToAll : To send the block created to all the authorities.
func (replica *Replica) SendToAll(bp Block) {
	newLong := replica.blockchains.LongestBlockchain().Append(bp)
	for i := range replica.authorities {
		if i < len(replica.authorities)-1 {
			Log("sent the updated block to:", replica.authorities[i])
			Log("height of the updated block:", bp.Height)
			go replica.Send(newLong, i)
		}

	}
}

// IsValidBlock : To check whether given block is valid
func (replica *Replica) IsValidBlock(block Block, previousBlock Block) bool {
	// Check for error in signature
	components := strings.Split(string(block.Signature), ":")
	if len(components) != 2 {
		return false
	}
	// Check for error in ParentHeader
	if len(block.ParentHeader) <= 1 {
		return false
	}
	// Check for error in Timestamp
	if block.Timestamp > time.Now().Unix() {
		return false
	}
	// Check for error in dependancy with parent block
	if previousBlock.Timestamp >= 0 && (previousBlock.Height != block.Height-1 || previousBlock.Timestamp > block.Timestamp) {
		return false
	}
	// Check for valid authorty
	indexOfAuthority := replica.IndexOf(block.Signature.Authority())
	if indexOfAuthority == IdenfityAuthority(block.Timestamp) {
		return true
	}
	return false
}

// ExisitngParent : To check whether a parent for the new block exisit in replica's blockchain
func (replica *Replica) ExisitngParent(block Block) bool {
	for _, blk := range replica.blockchains.LongestBlockchain().Blocks {
		if blk.Header == block.ParentHeader {
			return true
		}
	}
	Log("No exisitng parent for this block.", block)
	Log("Current blockchain: ", replica.blockchains.LongestBlockchain().Blocks)
	return false
}

// Run the Replica until the done channel is closed.
func (replica *Replica) Run(done <-chan struct{}) {

	for {
		select {
		case <-replica.blockGenerator:
			// 1. Generate the next Block in the blockchain whenever the
			//    blockGenerator channel signals that it is time to do so.
			currentTime := time.Now().Unix()
			if replica.IndexOf(replica.id) == IdenfityAuthority(currentTime) {
				newBlock := NewBlock(replica.blockchains.endOfLongestBlockchain.Header, replica.blockchains.endOfLongestBlockchain.Height+1, currentTime)
				newBlock = replica.Sign(newBlock)
				Log("Block created by:", replica.IndexOf(replica.id))
				replica.SendToAll(newBlock)
			}

		case query := <-replica.blockQueryReceiver:
			// 2. Respond to BlockQueries that received on the blockQueryReceiver
			//    channel.
			query.Responder <- replica.blockchains.LongestBlockchain().Range(query.Begin, query.End)
			Log("Recieved and responded to a query:", query)

		case recieved := <-replica.blockReceiver:
			//	3. Send Blocks to other Replicas using the conns channels, and
			//    validate Blocks received by other Replicas.
			Log("Recieved message with length:", len(recieved.Blocks))
			Log("Length of the blockchain I have:", len(replica.blockchains.LongestBlockchain().Blocks))
			var n int
			var validBlocks []Block
			// Not process the Incoming messages with block length less than the one replica has
			if len(replica.blockchains.LongestBlockchain().Blocks) > len(recieved.Blocks) {
				n = -1
				continue
			}
			// Finding the similarity between the current blockchain and the recieved one. Also adding
			// to the validBlocks
			for i := range replica.blockchains.LongestBlockchain().Blocks {
				if recieved.Blocks[i] != replica.blockchains.LongestBlockchain().Blocks[i] {
					n = i
					break
				}
				validBlocks = append(validBlocks, replica.blockchains.LongestBlockchain().Blocks[i])
			}
			if n < 1 {
				n = len(recieved.Blocks) - len(replica.blockchains.LongestBlockchain().Blocks)
			}
			var prevBlock Block
			prevBlock.Timestamp = -2 //as it initalizes to 0 in go
			condersLength := len(recieved.Blocks) - len(validBlocks) - 1
			contenders := recieved.LatestN(condersLength)
			updatedChain := false
			// Add each valid block to the replica's longest blockchain from list of new recived blocks
			for _, newBlock := range contenders.Blocks {
				if replica.IsValidBlock(newBlock, prevBlock) {
					validBlocks = append(validBlocks, newBlock)
					if replica.ExisitngParent(newBlock) {
						Log("The signature of the block added:", newBlock.Signature)
						replica.blockchains.ReplaceEndOfLongestBlockchain(newBlock)
						updatedChain = true
					}
				} else {
					Log("Error occured in one of the blocks. Processed length untill now: ", len(validBlocks))
					break
				}
			}
			// 4. Drop the connectivity to 0.25 and see if consensus make sure that
			//    consensus can still be reached.
			// When the gap between the replicas longest chain and the set of valid blocks recieved is huge,
			// add the blocks in recived message deleting the extra ones held by replica. A block is accepted only when is common in all chains.
			if !updatedChain && len(validBlocks)-len(replica.blockchains.LongestBlockchain().Blocks) > 2 {
				Log("-----------------GAP IS HUGE ------------------")
				replica.blockchains = NewBlockchains()
				for i, newBlock := range validBlocks {
					if i >= 1 {
						if replica.ExisitngParent(newBlock) {
							replica.blockchains.ReplaceEndOfLongestBlockchain(newBlock)
						} else {
							break
						}
					}

				}
				Log("Blockchain updated", replica.blockchains.LongestBlockchain())
			}
		// To stop when done channel is closed
		case <-done:
			return
		}

	}
}
