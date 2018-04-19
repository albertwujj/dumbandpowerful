
class Node:

    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def setLeft(self, node):
        self.left = node

    def getLeft(self):
        return self.left

    def setRight(self, node):
        self.right = node

    def getRight(self):
        return self.right

    def treeCopy(self):
        curr = self.nodeCopy()
        if self.left is not None:
            curr.left = self.left.treeCopy()
        if self.right is not None:
            curr.right = self.right.treeCopy()
        return curr

    def nodeCopy(self):
        return Node(self.data)

    #check if any node contains data
    def __contains__(self, data):
        if self.data == data:
            return True
        else:
            if self.left is not None and data in self.left:
                return True
            if self.right is not None and data in self.right:
                return True
            return False

    #flip left and right subtrees
    def flip(self):
        temp = self.right
        self.right = self.left
        self.left = temp