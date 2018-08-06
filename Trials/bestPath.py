_matrix = [[0 for y in range(5)] for x in range(7)]
_matrix[1][3]=-1
_matrix[2][2]=-1
_matrix[4][3]=-1
_matrix[4][2]=-1
_matrix[5][3]=-1
_matrix[5][4]=-1
_matrix[6][1]=-1

for x in range(7):
    print(_matrix[x])

traversal_map = {}

def getKey(x,y):
    return ""+str(x)+","+str(y)

def traversal(x,y):
    d_steps = -1
    r_steps = -1
    if(x==6 and y==4):
        return
    if(getKey(x,y) in traversal_map):
        return traversal_map.get(getKey(x,y))
    if(x+1<7 and _matrix[x+1][y]>=0):
        d_steps=traversal(x+1,y)
    if(y+1<5 and  _matrix[x][y+1]>=0):
        r_steps=traversal(x, y+1)
    if(d_steps == -1 and r_steps == -1):
        traversal_map[getKey(x,y)]=-1
    else:
        traversal_map[getKey(x,y)]=1

traversal(0,0)

def traverse(x,y):
    print(x,y)
    if(x+1 < 7 and _matrix[x+1][y]==1):
        return traverse(x+1,y)
    if(y+1 <5 and _matrix[x][y+1]==1):
        return traverse(x, y+1)

_matrix = [[traversal_map[getKey(x,y)] if getKey(x,y) in traversal_map else -1  for y in range(5)] for x in range(7)] 
traverse(0, _matrix[0].index(1))