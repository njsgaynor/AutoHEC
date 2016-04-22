# Create storage-outflow curves

from hec.heclib.dss import HecDss

def getStorageOutflowCurve(tableName, soPaths, soDss):
    u = tableName.split("_")

    for p in soPaths:
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(tableName)
        if (len(u[0]) > 1) and (u[0].upper() in p.upper()):
            try:
                float(u[1])
                soData = soDss.get(p, True)
                return list(soData.yOrdinates[0]), list(soData.xOrdinates)
            except ValueError:
                print(u[1])
                if (u[0].upper() + "_" + u[1].upper()) in p.upper():
                    soData = soDss.get(p, True)
                    return list(soData.yOrdinates[0]), list(soData.xOrdinates)
                else:
                    print("Doesn't fit conditions.", u[0:2])
        elif (len(u[0]) == 1) and ((u[0].upper() + "_" + u[1].upper()) in p.upper()):
            soData = soDss.get(p, True)
            return list(soData.yOrdinates[0]), list(soData.xOrdinates)
    return -1,-1


# NOTE: this function assumes the table is already in the DSS file (as outlined
# in step 6 of the example workflow)
def writeTable(tableName, storage, outflowRates):
    """Write a storage curve to the DSS file"""
    storageOutflowCurve = dss.get(tableName)
    storageOutflowCurve.xOrdinates = storage
    storageOutflowCurve.yOrdinates = [outflowRates]
    storageOutflowCurve.numberOrdinates = len(storage)
    dss.put(storageOutflowCurve)


# obtain configuration details for HEC applications for
# python and jython scripts
import hecConfig
reload(hecConfig)
config = hecConfig.HecConfig()
dssFilePath = config.getHmsProjectPath() + "/" + config.hmsProjectName + ".dss"
dss = HecDss.open(dssFilePath)
soDss = HecDss.open(config.osDssFile)


# Read the subbasin information from the pickle file saved by the calling script (hecModel.py)
import pickle
dtf = open(config.getDataTransferFilePath(),'r+')
subbasins = pickle.load(dtf)
dtf.close()

acresPerSqMile = 640

# Build and save the outflow-storage curve for each sub basin
for subbasin in subbasins:
    if not subbasin['tableName'] == '':
        print(subbasin['area'])
        soPath = "//*MWRD*/STORAGE-FLOW///TABLE/"
        soPathsAll = soDss.getCatalogedPathnames(soPath)
        outflowRates, storage = getStorageOutflowCurve(subbasin['tableName'], soPathsAll, soDss)
        writeTable("//" + subbasin['tableName'] + "/STORAGE-FLOW///TABLE/", storage, outflowRates)

dss.done()
