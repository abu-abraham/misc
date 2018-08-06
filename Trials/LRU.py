# The task is to design and implement methods of an LRU cache. The class has two methods get and set which are defined as follows.
# get(x)   : Gets the value of the key x if the key exists in the cache otherwise returns -1
# set(x,y) : inserts the value if the key x is not already present. If the cache reaches its capacity 
# it should invalidate the least recently used item before inserting the new item.
import math
import datetime


class Queue:
    values = [0] 
    heap_size = 1

    def _print(self):
        print(self.values)
    
    def parent(self, i):
        return int(i/2)

    def left(self, i):
        return 2*i

    def right(self, i):
        return self.left(i)+1

    def remove(self):
        v = self.values[1]
        self.values[1] = self.values[self.heap_size-1]
        self.values.pop(self.heap_size-1)
        self.heap_size-=1
        self.change(self.values[1], self.values[1])
        return v


    def insert(self, key):
        self.values.append(key)
        self.heap_size+=1
        self._sort(self.heap_size-1)

    def _sort(self, index):
        while index > 1 and (self.values[self.parent(index)] > self.values[index]):
            temp = self.values[self.parent(index)]
            self.values[self.parent(index)] = self.values[index]
            self.values[index] = temp
            index = self.parent(index)

    def get_index(self,index, key):
        print(key)
        if index < self.heap_size:
            if self.values[index] == key:
                return index
            if self.left(index) < self.heap_size and self.values[self.left(index)] <= key:
                return self.get_index(self.left(index), key)
            elif self.right(index) < self.heap_size and self.values[self.right(index)] < key:
                return self.get_index(self.right(index), key)
        return None

    def change(self, key, new_key):
        index = self.get_index(1, key)
        if index == None:
            return
        self.values[index] = new_key
        smallest = index
        if self.left(index) < self.heap_size and self.values[self.left(index)]< self.values[index]:
            smallest = self.left(index)
        if self.right(index) < self.heap_size and self.values[self.right(index)]<=self.values[smallest]:
            smallest = self.right(index)
        if smallest!=index:
            temp = self.values[smallest]
            self.values[smallest] = self.values[index]
            self.values[index] = temp
            self.change(smallest, self.values[smallest])


queue = Queue()

max_capacity = 10

_cache = {}
_map = {}
_queue = []

def remove():
    print("a")



def setValue(x,y):
    if len(_cache) == max_capacity:
        print("Remove", queue.remove())

    if x not in _cache:
        _cache[x] = y
        _queue.append([])
        t = datetime.datetime.now()
        _map[x] = t
        queue.insert(t)
    else:
        queue.change(_map.get(x), datetime.datetime.now())

        

def getValue(x):
    return _cache.get(x) if x in _cache else -1;


for i in range(13):
    setValue(i, "blah")