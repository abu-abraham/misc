import sys

storage = {}
limit = None

def countWays(_sum):
    if(_sum > limit):
        return 0;
    if(_sum == limit):
        return 1;
    if(_sum in storage):
        return storage.get(_sum)
    else:
        storage[_sum]= countWays(_sum+1)+countWays(_sum+2)+countWays(_sum+3)
        return storage.get(_sum)

def getInput(arg):
    val = 0;
    try:
        print(arg)
        val = int(arg[1])
    except:
        print("Enter number in digit as first argument")
    return val

if __name__ == "__main__":
    limit = getInput(sys.argv)
    print(countWays(0))
