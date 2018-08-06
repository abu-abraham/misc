_input = [3,5,4,2,6,7]

storage = {}
_min = _input[0]
_index = 0
for item, index in enumerate(_input):
    if _min > item:
        storage.setdefault(((index-1) -_index),[]).append([_index,index-1])
        _min = item
        _index = index
storage.setdefault(((index-2) -_index),[]).append([_index,index-2])
print(storage)

