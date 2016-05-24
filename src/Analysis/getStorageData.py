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
versions = config.versions
runName = config.hmsRunName

dataToGet = []
dssFiles = []
dataDict = {}
for v in versions:
    for j in dssFileName:
        dataToGet.append(["//*/STORAGE/*/*/RUN:" + runName + "/", "storage_V" + v])
        dssFiles.append(versionPath + v + j)
for i in range(len(dataToGet)):
    dssFile = HecDss.open(dssFiles[i], True)
    pathNames = dssFile.getCatalogedPathnames(dataToGet[i][0])
    for item in range(len(pathNames)):
        dataFromFile = dssFile.get(pathNames[item], True)
        try:
            dataList = list(dataFromFile.values)
            dataDict.update({pathNames[item]: dataList})
        except Exception, e:
            print("Could not retrieve storage data: " + dataToGet[i][0])
    try:
        outFile = open(filePath + dataToGet[i][1] + ".txt", 'wb')
    except Exception, e:
        print(e, "Invalid file name?")
    pickle.dump(dataDict, outFile)
    outFile.close()
