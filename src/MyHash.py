class MyHash(object):
    def __init__(self):
        self.st = set()

    def search(self, r):
        if tuple(r) in self.st:
            return True
        else:
            return False

    def insert(self, r):
        self.st.add(tuple(r))
