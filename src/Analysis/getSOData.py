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
filePath = config.filePath  #G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/
versionPath = config.versionPath  #Stony_V
dssFileName = config.dssHmsFileName # [self.dssHmsFilePath + "LucasDitch/LUDT_DesignRuns/LUDT_Design.dss", etc.
bVersions = config.baseVersions  #"1.0", "2.0", etc.
cVersions = config.compareVersions  #"1.0", "2.0", etc.

for v in range(len(bVersions)):
    bV = bVersions[v]
    cV = cVersions[v]
    dataToGet = []
    dssFiles = []
    dataDict = {}
    for j in dssFileName:
        dataToGet.append(["//*/STORAGE-FLOW///TABLE/", "storageoutflow_V" + bV])
        dssFiles.append(versionPath + bV + j)
    for i in range(len(dataToGet)):
        dssFile = HecDss.open(dssFiles[i], True)
        pathNames = dssFile.getCatalogedPathnames(dataToGet[i][0])
        for item in range(len(pathNames)):
            dataFromFile = dssFile.get(pathNames[item], True)
            try:
                dataList = [list(dataFromFile.xOrdinates), list(dataFromFile.yOrdinates[0])]
                dataDict.update({pathNames[item]: dataList})
                #print("added", pathNames[item])
            except:
                print("didn't work")
        outFile = open(filePath + dataToGet[i][1] + ".txt", 'wb')
        print(dataDict.keys())
        pickle.dump(dataDict, outFile)
        outFile.close()

    dataToGet = []
    dssFiles = []
    dataDict = {}
    for j in dssFileName:
        dataToGet.append(["//*/STORAGE-FLOW///TABLE/", "storageoutflow_V" + v + "optim"])
        dssFiles.append(versionPath + cV + j)
    for i in range(len(dataToGet)):
        dssFile = HecDss.open(dssFiles[i], True)
        pathNames = dssFile.getCatalogedPathnames(dataToGet[i][0])
        for item in range(len(pathNames)):
            dataFromFile = dssFile.get(pathNames[item], True)
            try:
                dataList = [list(dataFromFile.xOrdinates), list(dataFromFile.yOrdinates[0])]
                dataDict.update({pathNames[item]: dataList})
                #print("added", pathNames[item])
            except:
                print("didn't work")
        outFile = open(filePath + dataToGet[i][1] + ".txt", 'wb')
        print(dataDict.keys())
        pickle.dump(dataDict, outFile)
        outFile.close()
