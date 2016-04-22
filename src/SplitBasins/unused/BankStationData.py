### These methods are intended to be used within other programs. As such, the file storage may not be robust across
### different versions of Jython.

import pickle

from hec.heclib.dss import HecDss

from src.SplitBasins.unused.DSSDataDict_class import DSSDataDict


def dssSerialize(dataFromFile, sinkFile):
    # Writes data to a pickle file for use in subsequent script.
    pickle.dump(dataFromFile, sinkFile)
    pass

def getDSSData(pathNames, dssFile):
    dataDict = DSSDataDict()
    for item in range(len(pathNames)):
        dataFromFile = dssFile.get(pathNames[item], True)
        dataDict.add({pathNames[item], dataFromFile.values})
    return dataDict

def getTimestageData(sourceFile):
    # Read in hourly (or other periodic) STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
    # Example of data paths:
    # /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/
    # /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01JAN2007/1HOUR/HUFFQII_100YR12H/
    # .get([file path], True) returns data from all dates
    dssFile = HecDss.open(sourceFile, True)
    pathNames = dssFile.getCatalogedPathnames("/*/*/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/")
    dataDict = getDSSData(pathNames, dssFile)
    return dataDict

def getMaxstageData(sourceFile):
    # Read in hourly (or other periodic) LOCATION-ELEVATION//MAX STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
    # Example of data paths:
    # /E STONY CR DITCH E STONY CR DITCH//LOCATION-ELEV//MAX STAGE/HUFFQII_100YR12H/
    dssFile = HecDss.open(sourceFile, True)
    pathNames = dssFile.getCatalogedPathnames("/*/*/LOCATION-ELEV//MAX STAGE/HUFFQII_100YR12H/")
    dataDict = getDSSData(pathNames, dssFile)
    return dataDict

def getPeakTimeData(sourceFile):
    # Read in hourly (or other periodic) LOCATION-TIME//MAX STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
    # Example of data paths:
    # /E STONY CR DITCH E STONY CR DITCH//LOCATION-TIME//MAX STAGE/HUFFQII_100YR12H/
    dssFile = HecDss.open(sourceFile, True)
    pathNames = dssFile.getCatalogedPathnames("/*/*/LOCATION-TIME//MAX STAGE/HUFFQII_100YR12H/")
    dataDict = getDSSData(pathNames, dssFile)
    return dataDict

def getBankData(sourceFile):
    ### Not sure if this can be automated. Would only need to do it once for each watershed.
    pass
