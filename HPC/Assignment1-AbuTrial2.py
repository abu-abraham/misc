from __future__ import division
import sys
import numpy as np
import math
import ctypes
from threading import Timer,Thread,Event
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
        self.atoms = np.array(self.atoms,dtype="float64")
        
    

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

    def print_attributes(self):
        print ("Dimension of cube: "+str(N))
        print ("Total no of atoms: "+str(self.total_molecules))
        print ("Integration time step: "+str(self.tstep))
        print ("Number of steps: "+str(iter))
        print ("TIME           Total                    Kinetic                   Potential")
        print ("========================================================================================")
        


    def run(self):
        ji = 0
        start = time.time()
        self.initialize_lists()   
        self.print_attributes() 
        t_step = 0   


        while not self.stopped.wait(float(tstep)):
            ctypes_arrays = [np.ctypeslib.as_ctypes(array) for array in self.atoms]
            pointer_ar = (ctypes.POINTER(ctypes.c_double) * self.total_molecules)(*ctypes_arrays)
            c_funct = ctypes.CDLL("./libfoo.so")
            c_funct.potentialEnergy.restype = ctypes.c_double
            pot = c_funct.potentialEnergy(ctypes.c_int(self.total_molecules),pointer_ar)


            kin = self.total_kinetic_energy()
            tot = pot + kin
            print ('%f       %.6e             %.6e            %.6e' %(t_step,tot,kin,pot))

            ctypes_arrays = [np.ctypeslib.as_ctypes(array) for array in self.atoms]
            pointer_ar = (ctypes.POINTER(ctypes.c_double) * self.total_molecules)(*ctypes_arrays)

            ctypes_arrays1 = [np.ctypeslib.as_ctypes(array) for array in self.velocity]
            pointer_ar1 = (ctypes.POINTER(ctypes.c_double) * self.total_molecules)(*ctypes_arrays1)

            ctypes_arrays2 = [np.ctypeslib.as_ctypes(array) for array in self.acceleration]
            pointer_ar2 = (ctypes.POINTER(ctypes.c_double) * self.total_molecules)(*ctypes_arrays2)


            xc = ctypes.CDLL("./libfoo.so")
            xc.updateCoordinates_(ctypes.c_int(self.total_molecules),pointer_ar,ctypes.c_float(self.tstep),pointer_ar1,pointer_ar2)


            ji+=1
            t_step+=self.tstep
            if (ji>=int(iter)):
                print (time.time()-start)
                stopFlag.set()


if len(sys.argv)<5:
    print ("Enter 4 arguments")
    sys.exit()
utils = Utils()
N, R, tstep, iter = utils.get_values(sys.argv)


stopFlag = Event()
thread = Program(stopFlag,N,R,tstep,iter)
thread.start()