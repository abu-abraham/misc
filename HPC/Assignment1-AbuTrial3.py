from __future__ import division
import sys
import numpy as np
import math
import ctypes
from threading import Timer,Thread,Event
import time
#from vpython import *
import time

class Utils:

    def get_values(self,argv):
        return int(argv[1]),argv[2],argv[3],argv[4]

class Program(Thread):
    
    def __init__(self, event, N, R, tstep, iter):
        Thread.__init__(self)
        self.stopped = event
        self.total_molecules = N*N*N
        self.atoms = []     
        self.vpythonAtoms = [] 
        self.define_initial_positions()
        self.utils = Utils()
        self.potential_energy = 0
        self.tstep = float(tstep)
        self.velocity = []
        self.acceleration = []
        R = float(R)
        thk = 0.02
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
        print ("Total                    Kinetic                   Potential")
        print ("========================================================================================")
        
    
    # def show_in_vpython(self):
    #     for i,atom in enumerate(self.atoms):
    #         self.vpythonAtoms[i].pos=vector(atom[0],atom[1],atom[2])
    
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
                    # self.vpythonAtoms.append(sphere(pos=vector(i_pos,j_pos,k_pos),radius=(padding/2),color=color.blue))
    
        #self.atoms = np.array(self.atoms,dtype="float64")
        
    

    def initialize_lists(self):
        for _ in range(0,self.total_molecules):
            self.acceleration.append([0,0,0])
            self.velocity.append([0,0,0])
        
        self.velocity = np.array(self.velocity,dtype="float64")
        self.acceleration = np.array(self.acceleration,dtype="float64")
        
    
    def total_kinetic_energy(self):
        sum = 0
        for v in self.velocity:
            sum+=(np.dot(v,v)/2)
        return sum


        


    def run(self):
        ji = 0
        self.initialize_lists()   
        self.print_attributes() 

        while not self.stopped.wait(float(tstep)):

            time_start = time.time()
            
            kin = self.total_kinetic_energy()

            ctypes_arrays = [np.ctypeslib.as_ctypes(array) for array in np.array(self.atoms,dtype="float64")]
            pointer_ar = (ctypes.POINTER(ctypes.c_double) * self.total_molecules)(*ctypes_arrays)
            c_funct = ctypes.CDLL("./libfoo.so")
            c_funct.potentialEnergy.restype = ctypes.c_double
            pot = c_funct.potentialEnergy(ctypes.c_int(self.total_molecules),pointer_ar)


            tot = kin + pot
            print ('%.6e             %.6e            %.6e' %(tot,kin,pot))
            
            c_atom_pos =  np.array(self.atoms)
            ctypes_arrays = [np.ctypeslib.as_ctypes(array) for array in c_atom_pos]
            pointer_ar = (ctypes.POINTER(ctypes.c_double) * self.total_molecules)(*ctypes_arrays)

            c_vel = np.array(self.velocity)
            ctypes_arrays1 = [np.ctypeslib.as_ctypes(array) for array in c_vel]
            pointer_ar1 = (ctypes.POINTER(ctypes.c_double) * self.total_molecules)(*ctypes_arrays1)

            ctypes_arrays2 = [np.ctypeslib.as_ctypes(array) for array in np.array(self.acceleration)]
            pointer_ar2 = (ctypes.POINTER(ctypes.c_double) * self.total_molecules)(*ctypes_arrays2)


            xc = ctypes.CDLL("./libfoo.so")
            xc.updateCoordinates2(ctypes.c_int(self.total_molecules),pointer_ar,ctypes.c_float(self.tstep),pointer_ar1,pointer_ar2)
            
            self.velocity = c_vel
            self.atoms = c_atom_pos
            ji+=1

            t_end = time.time()
            #print("Time before iteration starts/pre-iteration time: %f seconds" %(t_end-time_start))
            #self.show_in_vpython()
            if (ji>=int(iter)):
                xc.manual_profiling()  
                stopFlag.set()


if len(sys.argv)<5:
    print ("Enter 4 arguments")
    sys.exit()
utils = Utils()
N, R, tstep, iter = utils.get_values(sys.argv)


stopFlag = Event()
thread = Program(stopFlag,N,R,tstep,iter)
thread.start()