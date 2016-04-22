from Element_class import Element
from Property_class import Property

class Reach(Element):
    def __init__(self):
        super(Reach, self).__init__('Reach', None)
        self.downstream = Property('Downstream')
        self.staticProperties = [self.downstream.getName()]

    @classmethod
    def readReach(cls, currentLine, basinsrc, basinsink):
        r = Reach()
        super(Reach, r).deserialize(currentLine, basinsrc)
        r.serialize(basinsink)
        return r

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Reach, self).add(self.downstream)
            else:
                super(Reach, self).add(a)
        else:
            print(a, "is not an instance of Property class. Cannot be added.")

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(None)
            else:
                try:
                    super(Reach, self).remove(a)
                except LookupError:
                    print("Property not found.")
