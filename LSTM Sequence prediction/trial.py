import numpy as np
import torch

#1000*4 matrix genertated. 4th column is the target
A = []
A = [[[0.2,0.2,0.1],[0.8,0.8,0.8],[(1000-i)/1000,(1000-i)/1000,(1000-i)/1000]] if i<80 else [[0.1,0.7,0.8],[0.8,0.8,0.8],[(1000-i)/1000,(1000-i)/1000,(1000-i)/1000]] for i in range(110)]

A = np.array(A).astype('float64')
torch.save(A, open('traindata.pt', 'wb'))
