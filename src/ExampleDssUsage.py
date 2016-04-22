# Example Jython script demonstrating how DSS data can be accessed
# within execution of HEC-DSSVue.

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

dssFilePath=config.getHmsProjectPath() + "/" + config.hmsProjectName + ".dss"
dss = HecDss.open(dssFilePath)

# examples of accessing and using flow data from DSS file
subbasinName="W28530"
subbasinDataPath="//" + subbasinName + "/FLOW-UNIT GRAPH/TS-PATTERN/5MIN/RUN:" + config.hmsRunName + "/"
inflowHydrograph = dss.get(subbasinDataPath.upper())
maxValueIdx = GetMaxValueIndex(inflowHydrograph)

# show various results
print("maximum inflow hydrograph value: %f" % max(inflowHydrograph.values))
print("maximum inflow hydrograph value at index %i is %f" % (maxValueIdx, inflowHydrograph.values[maxValueIdx]))
print dir(inflowHydrograph)
print inflowHydrograph.startTime
print inflowHydrograph.endTime
print inflowHydrograph.times

# example of writing a dummy curve to the DSS file
# NOTE: this relies on the tables (i.e. dummy tables) already existing
# in the DSS file (as outlined in step 6 of the example workflow) 
print dir(dss)
storageOutflowCurve = dss.get("//TABLE 1/STORAGE-FLOW///TABLE/")
storageOutflowCurve.xOrdinates = [1,2,3]
storageOutflowCurve.yOrdinates = [[1,2,3]]
storageOutflowCurve.numberOrdinates = 3
dss.put(storageOutflowCurve)
dss.done()
