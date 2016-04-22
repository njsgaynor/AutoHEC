from Element_class import Element
from Property_class import Property

class Junction(Element):
    def __init__(self):
        super(Junction, self).__init__('Junction', None)
        self.downstream = Property('Downstream')
        self.staticProperties = [self.downstream.getName()]

    @classmethod
    def readJunction(cls, currentLine, basinsrc, basinsink):
        j = Junction()
        super(Junction, j).deserialize(currentLine, basinsrc)
        j.serialize(basinsink)
        return j

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Junction, self).add(self.downstream)
            else:
                super(Junction, self).add(a)
        else:
            print(a, "is not an instance of Property class. Cannot be added.")

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(None)
            else:
                try:
                    super(Junction, self).remove(a)
                except LookupError:
                    print("Property not found.")

    @classmethod
    def newJunction(cls, s, basinsink):
        j = Junction()
        j.setIdentifier('JN ' + str(s.getIdentifier()))
        j.downstream = s.downstream
        p = Property.newProperty('Canvas X', s.canvasx.getValue())
        super(Junction, j).add(Property.newProperty('Canvas X', s.canvasx.getValue()))
        super(Junction, j).add(Property.newProperty('Canvas Y', s.canvasy.getValue()))
        super(Junction, j).add(j.downstream)
        j.serialize(basinsink)
        return j
