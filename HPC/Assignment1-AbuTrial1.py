from __future__ import division
import sys
import numpy as np
import math
from threading import Timer,Thread,Event


class Utils:
    def get_values(self,argv):
        return int(argv[1]),argv[2],argv[3],argv[4]

    def distance(self,x1,y1,z1,x2,y2,z2):
        x = math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2))+((z1-z2)*(z1-z2)))
        # a = np.array([x1,y1,z1])
        # b = np.array([x2,y2,z2])
        # y =  np.linalg.norm(a-b)
        # print str(x)+"   "+str(y)
        return x

class Program(Thread):
    
    def __init__(self, event, N, R, tstep, iter):
        Thread.__init__(self)
        self.stopped = event
        self.total_molecules = N*N*N
        self.molecules = np.ones(self.total_molecules)
        self.molecules = self.molecules.reshape([N,N,N])
        self.atoms = []
        self.define_initial_positions()
        self.utils = Utils()
        self.potential_energy = 0
        self.tstep = float(tstep)
        self.velocity = []
        self.acceleration = []        
        
    
    def define_initial_positions(self):
        dimensionality_factor = int(R)/int(N)
        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    self.atoms.append([i*dimensionality_factor,j*dimensionality_factor,k*dimensionality_factor])
        
        


    def find_potential(self,node):
        #print "Distances from "+str(xi)+" "+str(xj)+" "+str(xk);
        sum = 0
        for item in self.atoms:
            if item != node:
                r_ij=self.utils.distance(node[0],node[1],node[2],item[0],item[1],item[2])
                sum+=1/r_ij**12-2/r_ij**6

        return sum

    def get_potential_energy(self):
        sum = 0
        for node in self.atoms:
            sum+=self.find_potential(node)
        return sum

    def initialize_lists(self):
        for _ in range(0,self.total_molecules):
            self.acceleration.append([0,0,0])
            self.velocity.append([0,0,0])

    def force_cordinates(self,node):
        rij = 0
        Fx = 0
        Fy = 0
        Fz = 0
        for item in self.atoms:
            if not item == node:
                rij = self.utils.distance(node[0],node[1],node[2],item[0],item[1],item[2])
                const_quantity = (((12/rij)**14)-((12/rij)**8))
                Fx+=const_quantity*(node[0]-item[0])
                Fy+=const_quantity*(node[1]-item[1])
                Fz+=const_quantity*(node[2]-item[2])
        return Fx,Fy,Fz

    def update_coordinates(self):
        for i,node in enumerate(self.atoms):
            new_acceleration = list(self.force_cordinates(node))
            node[0] = node[0]+self.tstep*(self.velocity[i][0]+(self.tstep*self.acceleration[i][0])/2)
            node[1] = node[1]+self.tstep*(self.velocity[i][1]+(self.tstep*self.acceleration[i][1])/2)
            node[2] = node[2]+self.tstep*(self.velocity[i][2]+(self.tstep*self.acceleration[i][2])/2)

            self.velocity[i][0] = self.velocity[i][0] + self.tstep*(self.acceleration[i][0]+new_acceleration[0])/2
            self.velocity[i][1] = self.velocity[i][1] + self.tstep*(self.acceleration[i][1]+new_acceleration[1])/2
            self.velocity[i][2] = self.velocity[i][2] + self.tstep*(self.acceleration[i][2]+new_acceleration[2])/2

            self.acceleration[i] = new_acceleration

    def total_kinetic_energy(self):
        sum = 0
        for v in self.velocity:
            sum+=(np.dot(v,v)/2)
        return sum
        


    def run(self):
        ji = 0
        self.initialize_lists()
        prevKin = 0
        test = False
        while not self.stopped.wait(float(tstep)):
            print("At time step ")+str(ji)
            kin = self.total_kinetic_energy()
            pot = self.get_potential_energy()
            tot = kin + pot
            print str(kin)+"         "+str(pot)+"         "+str(tot)
            print self.atoms[0]
            if (test):
                if pot > kin:
                    print "Potential energy is greater"
                else:
                    print "Kinetic energy is greater"
                
                if prevKin > kin:
                    print "Previous kinetic energy is greater"
                else:
                    print "Present kinetic energy is greater"

                prevKin = kin
            self.update_coordinates()
            ji+=1
            if (ji>=int(iter)):
                stopFlag.set()
            # call a function


if len(sys.argv)<5:
    print "Enter 4 arguments"
    sys.exit()
utils = Utils()
N, R, tstep, iter = utils.get_values(sys.argv)


stopFlag = Event()
thread = Program(stopFlag,N,R,tstep,iter)
thread.start()