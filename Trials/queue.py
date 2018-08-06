
class Queue:
    values = [0] 
    heap_size = 1

    def _print(self):
        print(self.values)
    
    def parent(self, i):
        return int(i/2)

    def left(self, i):
        return 2*i

    def right(self, i):
        return self.left(i)+1

    def remove(self):
        v = self.values[1]
        self.values[1] = self.values[self.heap_size-1]
        self.values.pop(self.heap_size-1)
        self.heap_size-=1
        self.change(self.values[1], self.values[1])
        return v


    def insert(self, key):
        self.values.append(key)
        self.heap_size+=1
        self._sort(self.heap_size-1)

    def _sort(self, index):
        while index > 1 and (self.values[self.parent(index)] > self.values[index]):
            temp = self.values[self.parent(index)]
            self.values[self.parent(index)] = self.values[index]
            self.values[index] = temp
            index = self.parent(index)

    def get_index(self,index, key):
        if index < self.heap_size:
            if self.values[index] == key:
                return index
            if self.left(index) < self.heap_size and self.values[self.left(index)] <= key:
                return self.get_index(self.left(index), key)
            elif self.right(index) < self.heap_size and self.values[self.right(index)] < key:
                return self.get_index(self.right(index), key)
        return None

    def change(self, key, new_key):
        index = self.get_index(1, key)
        if index == None:
            return
        self.values[index] = new_key
        smallest = index
        if self.left(index) < self.heap_size and self.values[self.left(index)]< self.values[index]:
            smallest = self.left(index)
        if self.right(index) < self.heap_size and self.values[self.right(index)]<=self.values[smallest]:
            smallest = self.right(index)
        if smallest!=index:
            temp = self.values[smallest]
            self.values[smallest] = self.values[index]
            self.values[index] = temp
            self.change(smallest, self.values[smallest])


q = Queue()

q.insert(10)
q.insert(100)
q.insert(140)
q.insert(120)
q.insert(20)
q.insert(120)
q.insert(20)
q._print()
q.change(20,300)
#q._print()
print(q.remove())
print(q.remove())
print(q.remove())
q._print()