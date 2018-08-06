#Array, find degree which is maximum count of repeating integers. Then find subarray starting and ending in max count - Then return min subarray size

def answer(n, elements):
    value_map = {}
    key_map = {}
    best = 2;
    for index, element in enumerate(elements):
        value_map.setdefault(element, []).append(index);
        if len(value_map[element]) >= best:
            key_map.setdefault(len(value_map[element]),[]).append(element);
            best = len(value_map[element])
    #sorted_value_map = sorted(value_map.iteritems(), key=lambda (k,v): (v,k));
    #print sorted_value_map
    if(len(key_map) == 0):
        return 1;
    max_rep = key_map.get(key_map.keys()[len(key_map)-1])
    sub_array_length = []
    for item in max_rep:
        sub_array_length.append(max(value_map[item]) - min(value_map[item])+1)
    return min(sub_array_length)



print answer(6,[1,1,2,1,2,2]);