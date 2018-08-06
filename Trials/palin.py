_input = "SAadBCBAYop"

_matrix = [[1 if x == y else 0 for y in range(len(_input))] for x in range(len(_input))]

step = 1
while step<len(_input):
    for i in range(len(_input)-step):
        j = i+step
        if (_input[i]==_input[j]):
            _matrix[i][j]= _matrix[i+1][j-1]+2
        else:
            _matrix[i][j]=max(_matrix[i][j-1],_matrix[i+1][j])
    step+=1


print(_matrix[0][len(_input)-1])
print(_matrix)
