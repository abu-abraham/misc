# Name: Abu Abraham   
# Student Number: u6325322
# Course: COMP6464
# Assignment Number: 1
# Name of this file:md1.py
# I declare that the material I am submitting in this file is entirely my own work. I have not
# collaborated with anyone to produce it, nor have I copied it, in part or in full, from work
# produced by someone else. I have not given access to this material to any other student in this
# course.

from __future__ import division
import sys
import numpy as np
import math
from threading import Timer,Thread,Event
#from vpython import *


class Utils:
    def get_values(self,argv):
        return int(argv[1]),argv[2],argv[3],argv[4]

    def distance(self,x1,y1,z1,x2,y2,z2):
        x = math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2))+((z1-z2)*(z1-z2)))
        return x

class Program(Thread):
    
    def __init__(self, event, N, R, tstep, iter):
        Thread.__init__(self)
        self.stopped = event
        self.total_molecules = N*N*N
        self.molecules = np.ones(self.total_molecules)
        self.molecules = self.molecules.reshape([N,N,N])
        self.atoms = []     
        self.vpythonAtoms = [] 
        self.define_initial_positions()
        self.utils = Utils()
        self.potential_energy = 0
        self.tstep = float(tstep)
        self.velocity = []
        self.acceleration = [] 
        R = float(R)
        thk = 0.1
        mid_point = R/2
        end_point = R
        start_point = 0.0
        # box(pos=vector(mid_point, mid_point, start_point), length=R, height=R, width=thk, color = vector(0.7,0.7,0.7)) 
        # box(pos=vector(mid_point, start_point, mid_point), length=R, height=thk, width=R, color = vector(0.7,0.7,0.7)) 
        # box(pos=vector(mid_point, end_point, mid_point), length=R, height=thk, width=R, color = vector(0.7,0.7,0.7)) 
        # box(pos=vector(start_point, mid_point, mid_point), length=thk, height=R, width=R, color = vector(0.7,0.7,0.7)) 
        # box(pos=vector(end_point, mid_point, mid_point), length=thk, height=R, width=R, color = vector(0.7,0.7,0.7)) 
        
    def print_attributes(self):
        print ("Dimension of cube: "+str(N))
        print ("Total no of atoms: "+str(self.total_molecules))
        print ("Integration time step: "+str(self.tstep))
        print ("Number of steps: "+str(iter))
        print ("TIME           Total                    Kinetic                   Potential")
        print ("========================================================================================")
        

    def define_initial_positions(self):
        padding  = int(R)/(int(N)*2)
        dimensionality_factor = int(R)/int(N)
        for i in range(0,N):
            i_pos = (i*dimensionality_factor)+padding
            for j in range(0,N):
                j_pos = (j*dimensionality_factor)+padding
                for k in range(0,N):
                    k_pos = (k*dimensionality_factor)+padding
                    self.atoms.append([i_pos,j_pos,k_pos])
                    #self.vpythonAtoms.append(sphere(pos=vector(i_pos,j_pos,k_pos),radius=.2,color=color.blue))


    def find_potential(self,node,index):
        isum = 0
        for i,item in enumerate(self.atoms):
            if i<index:
                r_ij=self.utils.distance(node[0],node[1],node[2],item[0],item[1],item[2])
                isum=isum+(1/pow(r_ij,12)-2/pow(r_ij,6))
        return isum

    

    def get_potential_energy(self):
        sum = 0
        for index,node in enumerate(self.atoms):
            s=self.find_potential(node,index)
            sum = sum+s
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
                const_quantity = 12/pow(rij,14)-12/pow(rij,8)
                Fx+=const_quantity*(node[0]-item[0])
                Fy+=const_quantity*(node[1]-item[1])
                Fz+=const_quantity*(node[2]-item[2])
        return Fx,Fy,Fz

    def show_in_vpython(self):
        for i,atom in enumerate(self.atoms):
            self.vpythonAtoms[i].pos=vector(atom[0],atom[1],atom[2])


    def update_coordinates(self):
        X = []
        for _ in range(0,self.total_molecules):
            X.append([0,0,0])
        for i in range(0,len(self.atoms)):
            new_acceleration = list(self.force_cordinates(self.atoms[i]))
            X[i][0]= (self.atoms[i][0]+self.tstep*(self.velocity[i][0]+(self.tstep*self.acceleration[i][0])/2))
            X[i][1]=(self.atoms[i][1]+self.tstep*(self.velocity[i][1]+(self.tstep*self.acceleration[i][1])/2))
            X[i][2]=(self.atoms[i][2]+self.tstep*(self.velocity[i][2]+(self.tstep*self.acceleration[i][2])/2))

            self.velocity[i][0] = self.velocity[i][0] + self.tstep*(self.acceleration[i][0]+new_acceleration[0])/2
            self.velocity[i][1] = self.velocity[i][1] + self.tstep*(self.acceleration[i][1]+new_acceleration[1])/2
            self.velocity[i][2] = self.velocity[i][2] + self.tstep*(self.acceleration[i][2]+new_acceleration[2])/2
            self.acceleration[i] = new_acceleration
        self.atoms = X
        #self.show_in_vpython()

    def update_coordinates_2(self):
        X = []
        for _ in range(0,self.total_molecules):
            X.append([0,0,0])
        for i in range(0,len(self.atoms)):
            new_acceleration = list(self.force_cordinates(self.atoms[i]))
            X[i][0]=(self.atoms[i][0]+self.tstep*(self.velocity[i][0]+(self.tstep*new_acceleration[0])/2))
            X[i][1]=(self.atoms[i][1]+self.tstep*(self.velocity[i][1]+(self.tstep*new_acceleration[1])/2))
            X[i][2]=(self.atoms[i][2]+self.tstep*(self.velocity[i][2]+(self.tstep*new_acceleration[2])/2))

            self.velocity[i][0] = self.velocity[i][0] + self.tstep*(new_acceleration[0])
            self.velocity[i][1] = self.velocity[i][1] + self.tstep*(new_acceleration[1])
            self.velocity[i][2] = self.velocity[i][2] + self.tstep*(new_acceleration[2])
            self.acceleration[i] = new_acceleration
        self.atoms = X
        #self.show_in_vpython()
        

    def total_kinetic_energy(self):
        sum = 0
        for v in self.velocity:
            sum+=(np.dot(v,v)/2)
        return sum
        


    def run(self):
        ji = 0
        self.initialize_lists()
        self.print_attributes()
        t_step=0.000
        while not self.stopped.wait(float(tstep)):           
            kin = self.total_kinetic_energy()
            pot = self.get_potential_energy()
            tot = kin + pot
            print ('%f       %.6e             %.6e            %.6e' %(t_step,tot,kin,pot))       
            ji+=1
            t_step+=self.tstep
            self.update_coordinates_2()
            if (ji>=int(iter)):
                stopFlag.set()


if len(sys.argv)<5:
    print ("Enter 4 arguments")
    sys.exit()
utils = Utils()
N, R, tstep, iter = utils.get_values(sys.argv)


stopFlag = Event()
thread = Program(stopFlag,N,R,tstep,iter)
thread.start()