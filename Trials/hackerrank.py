

def isValid(A):
    _map  = {}

    for char in A:
        if char in _map:
            _map[char] = _map.get(char)+1
        else:
            _map[char] = 1
    value_map = {}

    for key in _map:
        value_map.setdefault(_map[key],[]).append(key)
    
    len_keys = len(value_map.keys())
    if len_keys > 2:
        return "NO"
    if len_keys == 1:
        return "YES"
    print(value_map)
    a = list(value_map.keys())[0]
    b = list(value_map.keys())[1]
    if not (a - b == 1 or a-b == -1):
        return "NO"
    a = len(value_map.get(a))
    b = len(value_map.get(b))
    if a == 1 or b == 1:
        return "YES"
    return "NO"

print(isValid("aabbcc"))

