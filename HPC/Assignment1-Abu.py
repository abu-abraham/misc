import sys
import numpy as np

def get_values(argv):
    return int(argv[1]),argv[2],argv[3],argv[4]

if len(sys.argv)<5:
    print "Enter 4 arguments"
N, R, tstep, iter = get_values(sys.argv);

total_molecules = N*N*N;
molecules = np.ones(total_molecules)
molecules = molecules.reshape([N,N,N])
print molecules
