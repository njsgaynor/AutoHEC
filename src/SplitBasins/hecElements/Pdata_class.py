from Element_class import Element
from Property_class import Property
from datetime import datetime
import calendar

class Pdata(Element):
    def __init__(self):
        super(Pdata, self).__init__('Table', None)
        self.dssfile = Property(None)
        self.pathname = Property(None)
        self.staticProperties = [self.dssfile.getName(), self.pathname.getName()]

    @classmethod
    def newPdata(cls, soname, pdatasink, dssfile):
        p = Pdata()
        # Add a new storage-outflow table to pdata
        nowDT = datetime.today()
        nowDate = str(nowDT.day) + ' ' + calendar.month_name[nowDT.month] + ' ' + str(nowDT.year)
        nowTime = str(nowDT.hour) + ':' + str(nowDT.minute) + ':' + str(nowDT.second)
        p.setIdentifier(soname)
        super(Pdata, p).add(Property.newProperty('Table Type', 'Storage-Outflow'))
        super(Pdata, p).add(Property.newProperty('Last Modified Date', str(nowDate)))
        super(Pdata, p).add(Property.newProperty('Last Modified Time', str(nowTime)))
        super(Pdata, p).add(Property.newProperty('X-Units', 'ACRE-FT'))
        super(Pdata, p).add(Property.newProperty('Y-Units', 'CFS'))
        super(Pdata, p).add(Property.newProperty('User External DSS File', 'NO'))
        super(Pdata, p).add(Property.newProperty('DSS File', dssfile))
        super(Pdata, p).add(Property.newProperty('Pathname', '//' + p.getIdentifier() + '/STORAGE-FLOW///TABLE/'))
        p.serialize(pdatasink)
