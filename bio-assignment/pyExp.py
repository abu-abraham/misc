import torch
from torch.autograd import Variable
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import random
from sklearn.model_selection import KFold
import sys
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from math import acos,degrees



class TwoLayerNet(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        super(TwoLayerNet, self).__init__()
        self.linear1 = torch.nn.Linear(D_in, H)
        self.relu =  torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(H, D_out)
        self.hrelu = None

    def forward(self, x):
        h_relu = self.linear1(x).clamp(min=0)
        y_pred = self.linear2(h_relu)
        self.hrelu = h_relu
        return y_pred

    def update(self, l1,l2,H,removed_list):
        self.linear1.weight = torch.nn.Parameter(l1.float())
        self.linear2.weight = torch.nn.Parameter(l2.float())
        # self.relu.weight = torch.nn.Parameter(r.float())
        self.linear1.out_features = H
        self.linear2.out_features = H
        f = self.linear1.bias.data.numpy()
        f = np.delete(f,removed_index,0)            
        self.linear1.bias=torch.nn.Parameter(torch.from_numpy(np.array(f)))


    

feature_name_map = {}
accuracy_theshold = .30
accuracy_theshold = 1- accuracy_theshold

test_set = None
frames = []
k = 10

validation_index = 0


def splitDataSet(data_frame):
    index = 0 
    mod_size = (len(data_frame)/k)
    for i in range(0,k):
        i_frame = pd.DataFrame()
        while index < ((i+1)*mod_size):
            i_frame = pd.concat([i_frame,data_frame.iloc[[index]]])
            index+=1
        frames.append(i_frame)

def testTrainAndValidationSets():
    global validation_index
    v_i = validation_index
    validation_set = frames[v_i]
    train_set = pd.DataFrame()
    for x, frame in enumerate(frames): 
        if x!=validation_index:
            train_set = pd.concat([train_set,frame])
    train_target = train_set['F20']
    train_features = train_set.drop('F20',axis=1)
    validation_target = validation_set['F20']
    validation_features = validation_set.drop('F20',axis=1)
    validation_index+=1
    return train_features,train_target,validation_features,validation_target


def evaluateTest():
    test_target = test_set['F20']
    test_features = test_set.drop('F20',axis=1)
    x = Variable(torch.from_numpy(np.array(test_features))).float()
    y = Variable(torch.from_numpy(np.array(test_target))).float()
    y_pred = model(x)
    y_pred = (y_pred > 0.5).float()
    loss_fn = torch.nn.L1Loss(size_average=False)
    loss_fraction = (int(loss_fn(y_pred,y))/len(test_target))
    print("Accuracy in test set, "+str(1-loss_fraction))


removed_index = []


def getReducedHiddenSize1(model):
    m = list(model.parameters())
    A = m[1].data.numpy()
    A = np.delete(A,removed_index,0)
    return (torch.from_numpy(np.array([A])))


def getSimilarUnits(model):
    global removed_index
    A = (model.hrelu).data.numpy()
    A= np.transpose(A)
    A_sparse = sparse.csr_matrix(A)
    similarities = cosine_similarity(A_sparse)
    similarities_sparse = cosine_similarity(A_sparse,dense_output=True)
    for k in range(0,A.shape[0]):
        for index, values in enumerate(similarities_sparse[k]):
            if index> k and (values>0.96 or values<-0.96) and index < A.shape[0]:
                if index not in removed_index:
                    removed_index.append(index)
                    A = np.delete(A,index,0)
    removed_index = list(set(removed_index))

def getReducedHiddenSize():
    m = list(model.parameters())
    A = m[0].data.numpy()
    print(A.shape)
    A = np.delete(A,removed_index,0)
    A= (torch.from_numpy(np.array(A)))
    return A


for i in range(1,21):
    feature_name_map['F'+str(i)] = "insert name"

data_frame = pd.read_csv('diabteic_rheno.csv', 
                  names = ['F1', 'F2', 'F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15','F16','F17','F18','F19','F20'])


print("Data frame has "+str(len(data_frame))+" elements")

data_frame = data_frame[data_frame.F1 != 0]

print("After removing F1 = 0, data frame has "+str(len(data_frame))+" elements")

N, D_in, H, D_out = 917, 19, 500, 1


splitDataSet(data_frame)

# t_i = random.randint(0,k-1)
# print("Test set sperated out")
# test_set = frames[t_i]
# del frames[t_i]



loss_fn = torch.nn.MSELoss(size_average=False)
learning_rate = 0.001

threshold_met = False
total_loss = 0
while threshold_met != True:
    H=500
    model = TwoLayerNet(D_in, H, D_out)
    train_features,train_target,validation_features,validation_target = testTrainAndValidationSets()

    x = Variable(torch.from_numpy(np.array(train_features))).float()
    y = Variable(torch.from_numpy(np.array(train_target))).float()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for t in range(1000):
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        if t==10:
            getSimilarUnits(model)
            for j,param in enumerate(model.parameters()):
                if j == 0:
                    A = getReducedHiddenSize()
                elif j==2:
                    C = getReducedHiddenSize1(model)
            
            H = A.shape[0]

            model.update(A,C,H,removed_index)
            optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
            removed_index = []
            print("Hidden layer size reduced to : "+str(H))
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    

    x = Variable(torch.from_numpy(np.array(validation_features))).float()
    y = Variable(torch.from_numpy(np.array(validation_target))).float()

    y_pred = model(x)
    y_pred = (y_pred > 0.5).float()
    loss_fn = torch.nn.L1Loss(size_average=False)
    
    total_loss += (int(loss_fn(y_pred,y))/len(validation_target))

    print("Validation set: "+str(validation_index)+" accuracy, "+str(1-(int(loss_fn(y_pred,y))/len(validation_target))))
    if validation_index >= k:
        loss_fraction = total_loss/(k)
        if loss_fraction < accuracy_theshold:
            threshold_met=True
            print("Validation accuracy > Threshold -- "+str(1-loss_fraction))
            #evaluateTest()
        else:
            print("Validation accuracy < Threshold -- "+str(1-loss_fraction))
            total_loss = 0
            validation_index=0


