import sys
import numpy as np
import math

N = 2
total_molecules = N*N*N
molecules = np.ones(total_molecules)
molecules = molecules.reshape([N,N,N])
initial_potential = 0
print "Atoms are at "
x = []
for i in range(0,N):
    for j in range(0,N):
        for k in range(0,N):
            print str(i)+" "+str(j)+" "+str(k)
            x.append([i,j,k]);

def distance(x1,y1,z1,x2,y2,z2):
    return math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2))+((z1-z2)*(z1-z2)))

def find_distance(node):
    #print "Distances from "+str(xi)+" "+str(xj)+" "+str(xk);
    sum = 0;
    for item in x:
        if item != node:
            sum+=distance(node[0],node[1],node[2],item[0],item[1],item[2])

    return sum;


for node in x: 
    print find_distance(node);

