

value_map = {}

def removeElement(item):
    value_map.pop(item,0);

def answer(n, elements):
    for element in elements:
        if element in value_map:
            value_map[element] = value_map[element]+element
        else:
            value_map[element]= element
    sorted_list = sorted(value_map.items(), key=lambda x: x[1],reverse=True)
    score = 0
    for item in sorted_list:
        if item[0] in value_map:
            score += item[1]
            removeElement(item[0]-1)
            removeElement(item[0]+1)
            

    return score




print answer(3,[3,4,2]);