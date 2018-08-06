A = [1,3,4,2,9]

def increment(pos):
    a = A[pos]
    a+=1
    A[pos]=a
    if(a==10):
        A[pos]=0
        increment(pos-1)

increment(len(A)-1)
print(A)
