from random import randint

class Node:
    left = None
    right = None
    value = None

node = Node()
node.value = randint(0,100)
root = node

for i in range(10):
    v = randint(0,100)
    v_n = Node()
    v_n.value = v
    ptr = root
    parent = root
    while (ptr!=None):
        parent = ptr
        if ptr.value > v:
            ptr = ptr.left
        else:
            ptr = ptr.right
    if(parent.value > v):
        parent.left = v_n
    else:
        parent.right = v_n

stac = []
stac.append(root)

upper_limit = 50
lower_limit = 25

a= set()

def _inorder(node):
    a.add(node.value)
    if node.left != None and node.left.value > lower_limit:
        _inorder(node.left)
    if node.right != None and node.right.value > lower_limit and node.right.value < upper_limit:
        _inorder(node.right)


if(root.value>lower_limit):
    _inorder(root)
else:
    _inorder(root.right)

print(a)



    


