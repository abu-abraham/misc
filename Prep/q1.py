
def answer(n, elements):
    value_map = {}
    for element in elements:
        binaryFormat =  "{0:b}".format(element)
        value_map.setdefault(binaryFormat.count('1'), []).append(element);
    #max_values_list = value_map[max(value_map.iterkeys())] --To get the largest key
    sorted_keys = value_map.keys()
    sorted_keys.sort()
    retun_list = []
    for k in sorted_keys:
        values = value_map[k]
        values.sort()
        retun_list+=values
    print retun_list

answer(5,[5,3,7,10,14]);