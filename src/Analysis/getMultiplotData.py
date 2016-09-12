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
dssFileName = config.dssRasFileName  #/HydraulicModels/ExistingConditions/STCR/STCR_DesignRuns/STCR_Design2.dss
versions = config.versions

dataToGet = []
dssFiles = {}
dataDict = {}
infile = open(filePath + "multipanel_plot_data_addresses.txt", 'rb')
dataAddresses = list(infile)
for i in range(len(dataAddresses)):
    dataAddresses[i] = dataAddresses[i].strip(('\r\n'))
print(dataAddresses)
# for v in versions:
#     for a in dataAddresses:
#         dataToGet.append([dataAddresses[a] + "FLOW/" + config.startDate + "/*", "hydrograph_V" + v])
#         dssFiles.append(versionPath + v + dssFileName)
for v in versions:
    dssFile = (versionPath + v + dssFileName)
    dssFiles[v] = HecDss.open(dssFile, True)
    dataDict[v] = {}
    for a in dataAddresses:
        pathNames = dssFiles[v].getCatalogedPathnames(a + "FLOW/" + config.startDate + "/*/" + config.rasRunName + "/")
        print(len(pathNames))
        for item in range(len(pathNames)):
            dataFromFile = dssFiles[v].get(pathNames[item], True)
            # try:
            dataList = list(dataFromFile.values)
            dataDict[v].update({a: dataList})
            # except Exception, e:
            #     for loc in range(len(dataFromFile.xOrdinates)):
            #         dataLocation = dataFromFile.xOrdinates[loc]#[:8]
            #         dataValue = dataFromFile.yOrdinates[0][loc]#[:8]
            #         splitPath = pathNames[item].split('/')
            #         splitPath[2] = str(dataLocation)
            #         fullLoc = "/".join(splitPath)
            #         dataDict.update({fullLoc: dataValue})
    outFile = open(filePath + "multipanel_plot_data.txt", 'wb')
    pickle.dump(dataDict, outFile)
    outFile.close()