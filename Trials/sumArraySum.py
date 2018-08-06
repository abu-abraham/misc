#Given an unsorted array of non-negative integers, 
# find a continuous sub-array which adds to a given number.

_input = [22,7,9,1,19,31,50,81]
target = 81
_sum = 0
queue = []
for item in _input:
    queue.append(item)
    _sum = _sum + item
    while(_sum>target):
        _sum = _sum - queue.pop(0)
    if(_sum==target):
        print(queue)
        queue= []
        _sum = 0