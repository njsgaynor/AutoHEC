class Property(dict):
    def __init__(self, name):
        super(Property, self).__init__()
        self[name] = None

    @classmethod
    def newProperty(cls, name, value):
        p = Property(name)
        p.setValue(value)
        return p

    def getValue(self):
        return self[self.getName()]

    def setValue(self, value):
        self[self.getName()] = value

    def getAsFloat(self):
        try:
            return float(self[self.getName()])
        except ValueError:
            print("Cannot convert to float.")

    def getAsString(self):
        try:
            return str(self[self.getName()])
        except ValueError:
            print("Cannot convert to string.")

    def getName(self):
        return self.keys()[0]

    def setName(self, name):
        self.name = name
