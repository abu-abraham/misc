
def answer(n, elements):
    A = [0]*(n+1)
    for i in range(0,len(elements)-1):
        for j in range(min(elements[i],elements[i+1]),max(elements[i],elements[i+1])+1):
            A[j]+=1;
    return A.index(max(A)) 

def answer1(n,elements):
    B = [0]*(n+2)
    for i in range(0,len(elements)-1):
        if elements[i] < elements[i+1]:
            B[elements[i]]+=1;
            B[elements[i+1]+1]-=1;
        else:
            B[elements[i]+1]-=1;
            B[elements[i+1]]+=1;
    max_val = 0
    max_indexes = []
    for i in range(1,len(B)):
        B[i]+=B[i-1]
        if B[i] >max_val:
            max_val = B[i]
            max_indexes = []
            max_indexes.append(i);
        elif B[i]==max_val:
            max_indexes.append(i);
    return min(max_indexes)
            





print answer1(10,[1,5,10,3]);