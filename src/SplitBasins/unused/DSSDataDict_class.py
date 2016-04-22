class DSSDataDict(dict):
    def __init__(self):
        super(dict, self).__init__()

    def add(self, x):
        self.update(x)

    def remove(self, x):
        del self[x]

    def getKeys(self):
        return self.keys()

    def getValues(self):
        return self.values()
