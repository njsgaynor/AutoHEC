# Example Jython script demonstrating how DSS data can be accessed
# within execution of HEC-DSSVue and obtain hydraulic results from
# a HEC-RAS DSS file.

def GetMaxValueIndex(hydrograph):
    # Gets the index of the entry in supplied
    # array with the largest value
    idx = 0
    max = float(-sys.maxint)
    for i in range (0, len(hydrograph.values)):
        if (hydrograph.values[i] > max):
            max = hydrograph.values[i]
            idx = i
    return idx

from hec.heclib.dss import HecDss

# obtain configuration details for HEC applications for
# python and jython scripts
import hecConfig
reload(hecConfig)
config = hecConfig.HecConfig()

dssFilePath=config.getRasProjectPath() + "/" + config.rasProjectName + ".dss"
dss = HecDss.open(dssFilePath)

hydraulicResults = {}

import pickle
dtf = open(config.getDataTransferFilePath(),'r+')
ditchNames = pickle.load(dtf)
dtf.close()

for ditchName in ditchNames:
    # get some flow data from the DSS file - obtain peak values
    dataPath = "/" + ditchName + "/FLOW/01DEC2006/1HOUR/" + config.rasPlanName + "/"
    dataHydrograph = dss.get(dataPath.upper(), True);  # true ensures entire time series is loaded
    maxValueIdx = GetMaxValueIndex(dataHydrograph)
    peakFlowValue = dataHydrograph.values[maxValueIdx]
    peakFlowTime = dataHydrograph.times[maxValueIdx]
    
    #print dataHydrograph.values
    #print maxValueIdx
    
    dataPath = "/" + ditchName + "/STAGE/01DEC2006/1HOUR/" + config.rasPlanName + "/"
    dataHydrograph = dss.get(dataPath.upper(), True);  # true ensures entire time series is loaded
    peakStageValue = max(dataHydrograph.values)

    hydraulicValues = {"peakFlowRate": peakFlowValue, "peakFlowTiming": peakFlowTime, "peakStage": peakStageValue}
    hydraulicResults[ditchName] = hydraulicValues;

# Write results to a intermediate file that can be read within the calling
# Python script as communicaton between Jython called from HEC software and
# Python is somewhat limited
#print hydraulicResults
dtf = open(config.getDataTransferFilePath(),'w')
dtf.write(str(hydraulicResults))
dtf.close()
