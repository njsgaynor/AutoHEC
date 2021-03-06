import sys
sys.path.append("C:/Users/nschiff2/IdeaProjects/AutoHEC/src/Analysis/")

from hec.heclib.dss import HecDss
import pickle
from Compare_Config import CompareConfig

# Read in hourly (or other periodic) STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
# Example of data paths:
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01JAN2007/1HOUR/HUFFQII_100YR12H/
# .getCatalogedPathnames([path pattern]) retrieves all data addresses that match the pattern
# .get([file path], True) returns data from all dates

config = CompareConfig()
filePath = config.filePath
dssFileName = config.dssRasFileName
dataPath = config.versionPath

print(config.scriptPath + "version.txt")
vFile = open(config.scriptPath + "version.txt")
vList = pickle.load(vFile)
vFile.close()
version = vList[0]
dataToGet = [["STAGE/" + config.startDate + "/*", "timestage"], ["LOCATION-ELEV//MAX STAGE", "maxstage"],
             ["LOCATION-TIME//MAX STAGE", "peaktime"]]
print(dataPath + version + dssFileName)
dssFile = HecDss.open(dataPath + version + dssFileName, True)
for i in range(len(dataToGet)):
    pathNames = dssFile.getCatalogedPathnames("/*/*/" + dataToGet[i][0] + "/" + config.rasRunName + "/")
    dataDict = {}
    for item in range(len(pathNames)):
        dataFromFile = dssFile.get(pathNames[item], True)
        try:
            dataList = list(dataFromFile.values)
            dataDict.update({pathNames[item]: dataList})
        except:
            for loc in range(len(dataFromFile.xOrdinates)):
                dataLocation = dataFromFile.xOrdinates[loc]#[:8]
                dataValue = dataFromFile.yOrdinates[0][loc]#[:8]
                splitPath = pathNames[item].split('/')
                splitPath[2] = str(dataLocation)
                fullLoc = "/".join(splitPath)
                dataDict.update({fullLoc: dataValue})
    print("Saving " + dataPath + version + dataToGet[i][1] + ".txt")
    outFile = open(dataPath + version + dataToGet[i][1] + ".txt", 'wb')
    pickle.dump(dataDict, outFile)
    outFile.close()