import sys
sys.path.append("C:/Users/nschiff2/IdeaProjects/AutoHEC/src/Analysis/")

from hec.heclib.dss import HecDss
import pickle
from Compare_Config import CompareConfig
import math

# Read in hourly (or other periodic) STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
# Example of data paths:
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01JAN2007/1HOUR/HUFFQII_100YR12H/
# .getCatalogedPathnames([path pattern]) retrieves all data addresses that match the pattern
# .get([file path], True) returns data from all dates

config = CompareConfig()
filePath = config.filePath  #G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/
versionPath = config.versionPath  #Stony_V
dssFileName = config.dssRasFileName  #/HydraulicModels/ExistingConditions/STCR/STCR_DesignRuns/STCR_Design2.dss
versions = config.versions

def roundSigfigs(num, sigfigs):
    """Round to specified number of sigfigs.
    from http://code.activestate.com/recipes/578114-round-number-to-specified-number-of-significant-di/
    accessed 3/24/2016"""
    if num != 0:
        return str(round(num, -int(math.floor(math.log10(abs(num))) - (sigfigs - 1))))
    else:
        return str(0.0)  # Can't take the log of 0

dataToGet = []
dssFiles = []
diffLocs = []
for v in versions:
    dataToGet.append(["LOCATION-ELEV//MAX STAGE", "peakElev_V" + v])
    dssFiles.append(versionPath + v + dssFileName) #(versionPath + i + " - Copy" + dssFileName)
    dataToGet.append(["LOCATION-TIME//MAX STAGE", "peakTime_V" + v])
    dssFiles.append(versionPath + v + dssFileName) #(versionPath + i + " - Copy" + dssFileName)
for j in range(len(dataToGet)):
    dssFile = HecDss.open(dssFiles[j], True)
    pathNames = dssFile.getCatalogedPathnames("/*/*/" + dataToGet[j][0] + "/" + config.rasRunName + "/")
    dataDict = {}
    for item in range(len(pathNames)):
        dataFromFile = dssFile.get(pathNames[item], True)
        try:
            dataList = list(dataFromFile.values)
            dataDict.update({pathNames[item]: dataList})
        except Exception, e:
            for loc in range(len(dataFromFile.xOrdinates)):
                dataLocation = dataFromFile.xOrdinates[loc]#[:8]
                dataValue = dataFromFile.yOrdinates[0][loc]#[:8]
                splitPath = pathNames[item].split('/')
                splitPath[2] = str(roundSigfigs(dataLocation, 7))
                fullLoc = "/".join(splitPath)
                dataDict.update({fullLoc: dataValue})
    print("Saving " + filePath + dataToGet[j][1] + ".txt")
    outFile = open(filePath + dataToGet[j][1] + ".txt", 'wb')
    pickle.dump(dataDict, outFile)
    outFile.close()