word_1 = "ABCDGH"
word_2 = "XAYBZD"

_matrix = [[0 for y in range(len(word_2))] for x in range(len(word_1))]

def valueOf(x,y):
    try:
        val = _matrix[x][y]
        return val
    except:
        return 0
        
for x in range(len(word_1)):
    for y in range(len(word_2)):
        if(word_1[x]==word_2[y]):
            _matrix[x][y] = max(valueOf(x-1,y), valueOf(x, y-1))+1
        else:
            _matrix[x][y] = max(valueOf(x-1,y), valueOf(x, y-1))

print(_matrix[len(word_1)-1][len(word_2)-1])