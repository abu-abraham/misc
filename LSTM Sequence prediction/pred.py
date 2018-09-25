from __future__ import print_function
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Sequence(nn.Module):
    def __init__(self):
        super(Sequence, self).__init__()
        self.lstm1 = nn.LSTMCell(3*3, 51)
        self.lstm2 = nn.LSTMCell(51, 51)
        self.linear = nn.Linear(51, 3)

    def forward(self, input, future = 0):
        outputs = []
        h_t = torch.zeros(input.size(0), 51, dtype=torch.double)
        c_t = torch.zeros(input.size(0), 51, dtype=torch.double)
        h_t2 = torch.zeros(input.size(0), 51, dtype=torch.double)
        c_t2 = torch.zeros(input.size(0), 51, dtype=torch.double)
        h_t, c_t = self.lstm1(input, (h_t, c_t))
        h_t2, c_t2 = self.lstm2(h_t, (h_t2, c_t2))
        output = self.linear(h_t2)
        outputs += [output]
        outputs = torch.stack(outputs, 1).squeeze()
        return outputs


if __name__ == '__main__':
    # set random seed to 0
    np.random.seed(0)
    torch.manual_seed(0)
    # load data and make training set
    data = torch.load('traindata.pt')
    entries = len(data)
    entries = entries if entries%2==0 else entries-1
    input = data[:entries-10, :]
    input = input.reshape(entries-10,9)
    input = torch.from_numpy(input)
    target = data[10:entries, 0]
    target = target.reshape(entries-10,3)
    target = torch.from_numpy(target)
    test_input = data[90:100, :]
    test_input = test_input.reshape(10,9)
    test_input = torch.from_numpy(test_input)
    test_target = data[100:110, 0]
    test_target = test_target.reshape(10,3)
    test_target = torch.from_numpy(test_target)
    # build the model
    seq = Sequence()
    seq.double()
    criterion = nn.MSELoss()
    # use LBFGS as optimizer since we can load the whole data to train
    optimizer = optim.LBFGS(seq.parameters(), lr=0.8)
    #begin to train
    for i in range(10):
        print('STEP: ', i)
        def closure():
            optimizer.zero_grad()
            out = seq(input)
            loss = criterion(out, target)
            #print('loss:', loss.item())
            loss.backward()
            return loss
        optimizer.step(closure)

    out = seq(test_input)
    loss = criterion(out, test_target)
    print("Output, ",out)
    print("LOSS, ", loss.data)
    # t = [[4.0,1.0,140.0],[4.0,1.0,130.0]]
    # t = torch.from_numpy(np.array(t))
    # print(test_input)
    # print(t)
    # out = seq(t)
    # print(out)
        
