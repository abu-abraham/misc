import torch
from torch.autograd import Variable
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

feature_name_map = {}
accuracy_theshold = .75
accuracy_theshold = 1- accuracy_theshold


#Train, Test and Validation split as .80,.10,.10
def testTrainAndValidationSets(data_frame):
    train_frame, check_frame = train_test_split(data_frame, test_size=0.2)
    test_frame, validation_frame = train_test_split(check_frame, test_size=0.5)
    train_target = train_frame['F20']
    train_features = train_frame.drop('F20',axis=1)
    test_target = test_frame['F20']
    test_features = test_frame.drop('F20',axis=1)
    validation_target = validation_frame['F20']
    validation_features = validation_frame.drop('F20',axis=1)
    return train_features,train_target,test_features,test_target,validation_features,validation_target


def evaluateTest(test_features,test_target):
    x = Variable(torch.from_numpy(np.array(test_features))).float()
    y = Variable(torch.from_numpy(np.array(test_target))).float()
    y_pred = model(x)
    y_pred = (y_pred > 0.5).float()
    loss_fn = torch.nn.L1Loss(size_average=False)
    loss_fraction = (int(loss_fn(y_pred,y))/len(test_target))
    print("Accuracy in test set, "+str(1-loss_fraction))


for i in range(1,21):
    feature_name_map['F'+str(i)] = "insert name"

data_frame = pd.read_csv('diabteic_rheno.csv', 
                  names = ['F1', 'F2', 'F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15','F16','F17','F18','F19','F20'])


print("Data frame has "+str(len(data_frame))+" elements")

data_frame = data_frame[data_frame.F1 != 0]

print("After removing F1 = 0, data frame has "+str(len(data_frame))+" elements")

N, D_in, H, D_out = 917, 19, 500, 1


model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    torch.nn.ReLU(),
    torch.nn.Linear(H, D_out),
)

loss_fn = torch.nn.MSELoss(size_average=False)
learning_rate = 0.001
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

threshold_met = False

while threshold_met != True:
    train_features,train_target,test_features,test_target,validation_features,validation_target = testTrainAndValidationSets(data_frame)
    x = Variable(torch.from_numpy(np.array(train_features))).float()
    y = Variable(torch.from_numpy(np.array(train_target))).float()
    for t in range(1000):
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        #print(t, loss.data[0])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    x = Variable(torch.from_numpy(np.array(validation_features))).float()
    y = Variable(torch.from_numpy(np.array(validation_target))).float()

    y_pred = model(x)

    y_pred = (y_pred > 0.5).float()


    loss_fn = torch.nn.L1Loss(size_average=False)
    
    loss_fraction = (int(loss_fn(y_pred,y))/len(validation_target))
    
    if loss_fraction < accuracy_theshold:
        threshold_met=True
        evaluateTest(test_features,test_target)
    else:
        print("Accuracy < Threshold -- "+str(1-loss_fraction))


