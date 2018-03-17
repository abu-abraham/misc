import math

def getDivisors(n) :
    i =1;
    divisors = []
    while i <= math.sqrt(n):
        if (n % i == 0 and i>1) :
            if (n / i == i) :
                divisors.append(i)
            else :
                divisors.append(i)
                divisors.append(n/i)
        i = i + 1
    return divisors

def answer(originList,destination):
    threshold = 1
    value_map ={}
    dest_map = {}
    for item in originList:
        if item > threshold: 
            org_facors = getDivisors(item)
            for dest in destination:
                if dest> threshold:
                    dest_factors = getDivisors(dest)
                    common = list(set(org_facors) & set(dest_factors))
                    dest_map[item] = common;
    print dest_map

print answer([1,2,4,6],[3,3,3,4])

