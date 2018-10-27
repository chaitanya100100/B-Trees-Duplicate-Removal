from bisect import bisect_right

class Node(object):
    def __init__(self, D = 256, keys = None, ptr = None, is_leaf = True):
        self.D = D
        self.ptr = []
        self.keys = []
        self.is_leaf = is_leaf

    def search(self, k):
        idx = bisect_right(self.keys, k)
        if idx != 0 and self.keys[idx-1] == k:
            return True
        elif not self.is_leaf:
            return self.ptr[idx].search(k)
        else:
            return False
        # for idx, ky in enumerate(self.keys):
        #     if ky == k:
        #         return True
        #     elif ky > k and self.ptr[idx] is not None:
        #         return self.ptr[idx].search(k)
        #
        # if len(self.keys) and self.keys[-1] < k and self.ptr[-1] is not None:
        #     return self.ptr[-1].search(k)
        return False

    def insert(self, k):
        # i = 0
        # while i < len(self.keys) and self.keys[i] <= k:
        #     i += 1
        i = bisect_right(self.keys, k)
        if self.is_leaf:
            self.keys.insert(i, k)
            self.ptr.insert(i, None)
        else:
            self.ptr[i].insert(k)
            if self.ptr[i].is_full():
                left, right, upk = self.ptr[i].split()

                old_node = self.ptr[i]

                self.keys.insert(i, upk)
                self.ptr[i] = left
                self.ptr.insert(i+1, right)

                del old_node

    def split(self):

        if self.is_leaf:
            left = Node(is_leaf=True)
            right = Node(is_leaf=True)
            at = self.D//2

            left.keys = self.keys[:at]
            right.keys = self.keys[at:]

            left.ptr = self.ptr[:at]
            right.ptr = self.ptr[at:]

            return left, right, self.keys[at]

        else:
            left = Node(is_leaf=False)
            right = Node(is_leaf=False)
            at = (self.D-1)//2

            left.keys = self.keys[:at]
            right.keys = self.keys[at+1:]

            left.ptr = self.ptr[:at+1]
            right.ptr = self.ptr[at+1:]

            return left, right, self.keys[at]

    def traverse(self, d=0):
        # i = 0
        # while i < len(self.keys):
        #     if not self.is_leaf:
        #         self.ptr[i].traverse()
        #     print(self.keys[i])
        #     i+=1
        # if not self.is_leaf:
        #     self.ptr[i].traverse()
        st = "depth %d : " % d
        for k in self.keys:
            st += str(k) + " "
        print(st)
        for p in self.ptr:
            if p is not None:
                p.traverse(d+1)

    def is_full(self):
        # print(len(self.ptr), self.is_leaf, self.D)
        return len(self.ptr) + self.is_leaf > self.D

class BTree(object):
    def __init__(self):
        self.root = Node(is_leaf=True)

    def search(self, k):
        return self.root.search(k)

    def insert(self, k):
        self.root.insert(k)
        if self.root.is_full():
            left, right, upk = self.root.split()
            old_root = self.root

            self.root = Node(is_leaf=False)
            self.root.keys.append(upk)
            self.root.ptr.append(left)
            self.root.ptr.append(right)

            del old_root

    def traverse(self):
        self.root.traverse()

if __name__ == "__main__":

    tree = BTree()
    while True:
        op, k = input().rstrip().split()
        if op == "a":
            tree.insert(int(k))
        elif op == "s":
            print(tree.search(int(k)))
        print("\n")
        tree.traverse()
        print("\n")
