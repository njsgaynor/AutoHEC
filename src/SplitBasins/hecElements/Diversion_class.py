from Element_class import Element
from Property_class import Property

class Diversion(Element):
    def __init__(self):
        super(Diversion, self).__init__('Diversion', None)
        self.downstream = Property('Downstream')
        self.divertto = Property('Divert To')
        self.staticProperties = [self.downstream.getName(), self.divertto.getName()]

    @classmethod
    def readDiversion(cls, currentLine, basinsrc, basinsink):
        d = Diversion()
        super(Diversion, d).deserialize(currentLine, basinsrc)
        d.serialize(basinsink)
        return d

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Diversion, self).add(self.downstream)
            elif a.getName() == self.divertto.getName():
                self.divertto.setValue(a.getValue())
                super(Diversion, self).add(self.divertto)
            else:
                super(Diversion, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(None)
            elif a.getName() == self.divertto.getName():
                self.divertto.setValue(None)
            else:
                try:
                    super(Diversion, self).remove(a)
                except LookupError:
                    print("Property not found.")
