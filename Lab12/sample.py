# ------------------------------------------------
# List
# ------------------------------------------------
#a=[1,2,3,4,5,6]
#a[0]               # => 1
#len(a)             # => 6
#a[2:4]             # => [3, 4]
#a[1:]              # => [2, 3, 4, 5, 6]
#a[:3]              # => [1, 2, 3]
#a[:-1]             # => [1, 2, 3, 4, 5]
#a[:-2]             # => [1, 2, 3, 4]
#b=[6,5,4,3,2,1]    
#a+b                # => [1, 2, 3, 4, 5, 6, 6, 5, 4, 3, 2, 1]
#a[0]+b[-1]         # => 2
#[a[0]]+[b[-1]]     # => [1, 1]

# ------------------------------------------------
# Linked List
# ------------------------------------------------
class Node(object):
    def __init__(self,data=0):
        self.value = data
        self.next = None
    def insert(self,data):
        temp = self
        while temp.next is not None:
            temp = temp.next
        temp.next = Node(data)                
    def printList(self):
        temp = self
        while temp is not None:
            print( temp.value, end=', ')
            temp = temp.next
        print()

# ------------------------------------------------
head = Node(1)
head.insert(2)
head.insert(3)
head.insert(4)
head.insert(5)
head.insert(6)
head.printList()    # => 1, 2, 3, 4, 5, 6,




