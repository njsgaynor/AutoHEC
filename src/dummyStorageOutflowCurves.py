import sys
sys.path.append("C:/Users/nschiff2/Documents/MWRDGC_WSRR/Optimatics/optimizer-hecras-integration/src/HEC-DSSVue/java/bin/java.exe")
#sys.path.append("C:/Program Files (x86)/Java/jdk1.8.0_72/src/java")
sys.path.append("C:/Users/nschiff2/Documents/MWRDGC_WSRR/Optimatics/optimizer-hecras-integration/src/HEC-DSSVue/java")
sys.path.append("C:/Program Files/Java/javahelp-2.0.05.jar")
sys.path.append("C:/Users/nschiff2/Documents/MWRDGC_WSRR/Optimatics/optimizer-hecras-integration/src/HEC-DSSVue/lib")
sys.path.append("C:/Users/nschiff2/Documents/MWRDGC_WSRR/Optimatics/optimizer-hecras-integration/src")

from hec.script import *
from hec.heclib.dss import HecDss
from hec.heclib.util import *
from hec.io import *
import java
import pickle

import hecConfig
reload(hecConfig)
config = hecConfig.HecConfig()

try:
    dtf = open(config.getDataTransferFilePath(),'r+')
    tableList = pickle.load(dtf)
    dtf.close()
    for item in range(len(tableList)):
        loc = tableList[item][1]
        watershed = "Testingonly"
        xParam = "STORAGE"
        yParam = "FLOW"
        type= "TABLE"
        stages = [0, 0.4, 0.5, 1.0, 2.0, 5.0, 10.0, 12.0]
        flows = [0, 0.1, 3, 11, 57, 235, 1150, 3700]
        pdc = PairedDataContainer()
        pdc.watershed = watershed
        pdc.location = loc
        pdc.fullName= "//%s/%s-%s///%s/" % \
                      ( loc, xParam, yParam, type)
        pdc.xOrdinates = stages
        pdc.yOrdinates = [flows]
        pdc.numberCurves = 1
        pdc.numberOrdinates = len(stages)
        pdc.labelsUsed = False
        pdc.xunits = "ACRE-FT"
        pdc.yunits = "CFS"
        pdc.xtype = "UNT"
        pdc.ytype = "UNT"
        pdc.xparameter = xParam
        pdc.yparameter = yParam
        pdc.transformType = 2
        dssFilePath=config.getHmsProjectPath() + "/" + config.hmsProjectName + ".dss"
        myDss = HecDss.open(dssFilePath)
        myDss.put(pdc)
        myDss.done()
except Exception, e:
    print(type(e))
    MessageBox.showError(' '.join(e.args), "Python Error")
except java.lang.Exception, e:
    print(type(e))
    MessageBox.showError(e.getMessage(), "Error")
