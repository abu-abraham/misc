import math


threshold = 1


def getDivisors(n) :
    i =1;
    divisors = []
    while i <= math.sqrt(n):
        if (n % i == 0) :
            if (n / i == i) :
                divisors.append(i)
            else :
                divisors.append(i)
                divisors.append(n/i)
        i = i + 1
    divisors = [i for i in divisors if i>threshold]
    return divisors

def bfs(val_map,start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(val_map[vertex] - visited)
    return list(visited)

def answer(originList,destination):
    value_map ={}
    total_list = originList+destination
    total_list = list(set(total_list))
    for item in total_list:
        if item > threshold: 
            org_facors = getDivisors(item)
            for dest in total_list:
                if dest > threshold and dest != item:
                    dest_factors = getDivisors(dest)
                    common = list(set(org_facors) & set(dest_factors))
                    if len(common)>0:
                        value_map.setdefault(item,[]).append(dest)
    for key in value_map:
        value_map[key]=set(value_map[key])
    dest_list = []
    for index, org in enumerate(originList):
        if org in value_map:
            if destination[index] in bfs(value_map,org):
                dest_list.append(1)
        else:
            dest_list.append(0)
    print dest_list
        



print answer([1,2,4,6],[3,3,3,4])



