import ctypes
import numpy
import sys

def working_example():
    testlib = ctypes.cdll.LoadLibrary('./abuTrialC.so')

    n=5
    outa = numpy.zeros(n,numpy.float)
    ina = numpy.linspace(1.0,200.0,n)

    print "initial array",ina
    testlib.square_array.restype = None
    testlib.square_array(ctypes.c_int(n),
                        numpy.ctypeslib.as_ctypes(ina),
                        numpy.ctypeslib.as_ctypes(outa))
    print "final array",outa

def my_attempt():
    testlib = ctypes.cdll.LoadLibrary('./abuTrialC.so')

    n=5
    outa = numpy.zeros(n)
    ina = numpy.linspace(1.0,200.0,n)

    print "initial array",ina
    testlib.square_array.restype = None
    testlib.square_array(ctypes.c_int(n),
                        numpy.ctypeslib.as_ctypes(ina),
                        numpy.ctypeslib.as_ctypes(outa))
    print "final array",outa


#my_attempt()

count = 5
size = 3

#create some arrays
arrays = [numpy.arange(size,dtype="float32") for ii in range(count)]
arrays = numpy.array([[1,2,3],[0,0,0],[1,1,1],[2,2,2],[3,1,1]],dtype="float32") 
print arrays


#get ctypes handles
ctypes_arrays = [numpy.ctypeslib.as_ctypes(array) for array in arrays]

#Pack into pointer array
pointer_ar = (ctypes.POINTER(ctypes.c_float) * count)(*ctypes_arrays)

print arrays

ctypes.CDLL("./libfoo.so").foo(ctypes.c_int(count),4, pointer_ar, ctypes.c_int(size))

print arrays

# import sys
# import numpy as np
# import math

# # from subprocess import check_output
# # x = check_output('./compute', shell=True)
# # print x


# import subprocess

# p = subprocess.Popen('./compute 1 2 3 4 5 6', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# for line in p.stdout.readlines():
#     print str(line)
# retval = p.wait()