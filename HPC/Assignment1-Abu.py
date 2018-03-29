import sys
import numpy as np
import math
from threading import Timer,Thread,Event

def get_values(argv):
    return int(argv[1]),argv[2],argv[3],argv[4]

def distance(x1,y1,z1,x2,y2,z2):
    return math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2))+((z1-z2)*(z1-z2)))

def find_distance(xi,xj,xk):
    #print "Distances from "+str(xi)+" "+str(xj)+" "+str(xk);
    sum = 0;
    for i in range(0,N):
        for j in range(0,N):
            for k in range(0,N):
                if not (xi == i and xj == j and xk == k):
                    sum+=distance(xi,xj,xk,i,j,k)
    print sum
    return sum;

def find_force(xi,xj,xk):
    print "ATOM FORCES"
    rij = 0
    Fx = 0
    Fy = 0
    Fz = 0
    for i in range(0,N):
        for j in range(0,N):
            for k in range(0,N):
                if not (xi == i and xj == j and xk == k):
                    rij = distance(xi,xj,xk,i,j,k)
                    const_quantity = (((12/rij)**14)-((12/rij)**8))
                    Fx+=const_quantity*(xi-i)
                    Fy+=const_quantity*(xj-j)
                    Fz+=const_quantity*(xk-k)
    return Fx,Fy,Fz



if len(sys.argv)<5:
    print "Enter 4 arguments"
N, R, tstep, iter = get_values(sys.argv)

total_molecules = N*N*N
molecules = np.ones(total_molecules)
molecules = molecules.reshape([N,N,N])
initial_potential = 0
print "Atoms are at "
for i in range(0,N):
    for j in range(0,N):
        for k in range(0,N):
            print str(i)+" "+str(j)+" "+str(k)
            initial_potential+=find_distance(i,j,k)

print initial_potential
for i in range(0,N):
    for j in range(0,N):
        for k in range(0,N):
            Fx, Fy, Fz  = find_force(i,j,k)
            print "New cordinates"
            new_i = i+1*(0+(1*Fx)/2)
            new_j = j+1*(0+(1*Fy)/2)
            new_k = k+1*(0+(1*Fz)/2)

            print str(new_i)+" "+str(new_j)+" "+str(new_k)
            
class MyThread(Thread):
    
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        ji = 0
        while not self.stopped.wait(1):
            print("At time step ")+str(ji)
            ji+=1;
            if (ji==20):
                stopFlag.set()
            # call a function

# stopFlag = Event()
# thread = MyThread(stopFlag)
# thread.start()
# # this will stop the timer










