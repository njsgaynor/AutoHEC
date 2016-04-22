class SBList(list):
    def __init__(self):
        super(list, self).__init__()

    def newItem(self, n, rr, a, tN):
        ditem = {}
        ditem["tableName"] = tN
        ditem["releaseRate"] = rr
        ditem["area"] = a
        ditem["name"] = n
        self.append(ditem)

    def remove(self, x):
        del self[x]

    def writeSbPairs(self, sbOut):
        import json
        with open(sbOut, 'wb') as dumpFile:
            json.dump(self, dumpFile)
