from Element_class import Element
from Property_class import Property
from Junction_class import Junction
from Reservoir_class import Reservoir
import copy

class Subbasin(Element):
    def __init__(self):
        super(Subbasin, self).__init__('Subbasin', None)
        self.area = Property('Area')
        self.downstream = Property('Downstream')
        self.curvenum = Property('Curve Number')
        self.impervious = Property('Percent Impervious Area')
        self.canvasx = Property('Canvas X')
        self.canvasy = Property('Canvas Y')
        self.canopy = Property('Canopy')
        self.rlsrate = Property('Release Rate')
        self.redevel = Property('Percent Redevelopment')
        self.staticProperties = [self.area.getName(), self.downstream.getName(), self.curvenum.getName(),
                                 self.impervious.getName(), self.canvasx.getName(), self.canvasy.getName(),
                                 self.canopy.getName(), self.rlsrate.getName(), self.redevel.getName()]

    @classmethod
    def readSubbasin(cls, currentLine, basinsrc, basinsink, redevel, curvenum, rlsrate):
        s = Subbasin()
        super(Subbasin, s).deserialize(currentLine, basinsrc)
        sNew, soname = s.divideSubbasin(basinsink, redevel, curvenum, rlsrate)
        s.rlsrate.setValue(rlsrate)
        s.redevel.setValue(redevel)
        s.serialize(basinsink)
        return s, sNew, soname

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.area.getName():
                self.area.setValue(a.getAsFloat())
                super(Subbasin, self).add(self.area)
            elif a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Subbasin, self).add(self.downstream)
            elif a.getName() == self.curvenum.getName():
                self.curvenum.setValue(a.getAsFloat())
                super(Subbasin, self).add(self.curvenum)
            elif a.getName() == self.impervious.getName():
                self.impervious.setValue(a.getAsFloat())
                super(Subbasin, self).add(self.impervious)
            elif a.getName() == self.canvasx.getName():
                self.canvasx.setValue(a.getValue())
                super(Subbasin, self).add(self.canvasx)
            elif a.getName() == self.canvasy.getName():
                self.canvasy.setValue(a.getValue())
                super(Subbasin, self).add(self.canvasy)
            elif a.getName() == self.canopy.getName():
                self.canopy.setValue(a.getValue())
                super(Subbasin, self).add(self.canopy)
            else:
                super(Subbasin, self).add(a)
        else:
            print(a, "is not an instance of Property class. Cannot be added.")

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == self.area.getName():
                self.area.setValue(None)
            elif a.getName() == self.downstream.getName():
                self.downstream.setValue(None)
            elif a.getName() == self.curvenum.getName():
                self.curvenum.setValue(None)
            elif a.getName() == self.impervious.getName():
                self.impervious.setValue(None)
            elif a.getName() == self.canvasx.getName():
                self.canvasx.setValue(None)
            elif a.getName() == self.canvasy.getName():
                self.canvasy.setValue(None)
            elif a.getName() == self.canopy.getName():
                self.canopy.setValue(None)
            else:
                try:
                    super(Subbasin, self).remove(a)
                except LookupError:
                    print("Property not found.")

    def divideSubbasin(self, basinsink, redevel, curvenum, rlsrate):
        #may need to be modified once I figure out exactly how this will be used
        j = Junction.newJunction(self, basinsink)
        r = Reservoir.newReservoir(self, basinsink, redevel, rlsrate)
        sNew = Subbasin.newSubbasin(self, basinsink, redevel, curvenum)
        self.area.setValue(self.area.getAsFloat() - sNew.area.getAsFloat())
        self.downstream.setValue('JN ' + self.getIdentifier())
        sNew.rlsrate.setValue(rlsrate)
        sNew.redevel.setValue(redevel)
        return sNew, r.storageoutflow.getAsString()

    @classmethod
    def newSubbasin(cls, s, basinsink, redevel, curvenum):
        sNew = copy.deepcopy(s)
        sNew.setIdentifier(s.getIdentifier() + 'MWRD')
        sNew.area.setValue((redevel / 100.) * s.area.getAsFloat())
        sNew.downstream.setValue('Reservoir ' + s.getIdentifier())
        sNew.canopy.setValue('SMA')
        # Define new canopy properties
        initCanopy = Property.newProperty('Initial Canopy Storage Percent', 0)
        maxCanopy = Property.newProperty('Canopy Maximum Storage', 0.52)
        endCanopy = Property.newProperty('End Canopy', '')
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, endCanopy)
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, maxCanopy)
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, initCanopy)
        sNew.curvenum.setValue(curvenum)
        sNew.serialize(basinsink)
        return sNew
