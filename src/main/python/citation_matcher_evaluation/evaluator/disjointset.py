class DisjointSet:
    def __init__(self):
         self.parent = self
         self.rank = 0

    def union(self, other):
         xRoot = self.find()
         yRoot = other.find()
         if xRoot.rank > yRoot.rank:
             yRoot.parent = xRoot
         elif xRoot.rank < yRoot.rank:
             xRoot.parent = yRoot
         elif xRoot != yRoot: # Unless x and y are already in same set, merge them
             yRoot.parent = xRoot
             xRoot.rank = xRoot.rank + 1

    def find(self):
         if self.parent == self:
            return self
         else:
            self.parent = self.parent.find()
            return self.parent
