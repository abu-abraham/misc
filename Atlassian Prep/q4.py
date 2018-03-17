
def answer(n, elements):
    A = [0]*(n+1)
    for i in range(0,len(elements)-1):
        for j in range(min(elements[i],elements[i+1]),max(elements[i],elements[i+1])+1):
            A[j]+=1;
    return A.index(max(A))




print answer(10,[1,5,10,3]);