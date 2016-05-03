# Create storage-outflow curves

from hec.heclib.dss import HecDss

def indexOfMaxValue(hydrograph):
    """returns the index of the largest entry in the given hydrograph"""
    assert(len(hydrograph.values) > 0)

    idx = 0
    max = float(-sys.maxint)
    for i in range (0, len(hydrograph.values)-1):
        if (hydrograph.values[i] > max):
            max = hydrograph.values[i]
            idx = i
    return idx, max

def findFirst(sequence, predicate):
    """find the index of the first element in the sequence where the predicate is true"""
    assert(len(sequence) > 0)
    for i in range(0, len(sequence)-1):
        if predicate(sequence[i]):
            return i

def findLast(sequence, predicate):
    """find the index of the last element in the sequence where the predicate is true"""
    assert(len(sequence) > 0)
    for i in range(len(sequence)-1, 0, -1):
        if predicate(sequence[i]):
            return i

def findFirstAfterPeak(peak, sequence, predicate):
    """find the index of the last element in the sequence where the predicate is true"""
    assert(len(sequence) > 0)
    for i in range(peak, len(sequence)-1):
        if predicate(sequence[i]):
            return i-1

def any(predicate, container):
    """Returns true if the predicate returns true on any element in the container"""
    for x in container:
        if predicate(x):
            return True
    return False

def flowFileDates(hmsRunName):
    #will not be accurate if there is more than one set of data--specify start date in config file?
    """Find the dates of any FLOW files in the DSS catalog"""
    from java.text import SimpleDateFormat
    dateFormat = SimpleDateFormat("ddMMMyyyy")
    print("Getting dates from " + hmsRunName + "...")

    dates = []
    #print(dss.getCatalogedPathnames())
    flowFiles = filter(lambda f:((f.split('/')[3] == 'FLOW') and (f.split('/')[6] == ('RUN:'+hmsRunName.upper()))),
                       dss.getCatalogedPathnames())
    #print(flowFiles)
    candidateDates = map(lambda x:x.split('/')[4], flowFiles)
    #print(candidateDates)

    for d in candidateDates:
        if d[0:2].isdigit() and d[2:5].isalpha() and d[5:9].isdigit():
            date = dateFormat.parse(d)
            dateAlreadyFound = any(lambda x:x.equals(date), dates)
            if not dateAlreadyFound:
                dates.append(date)

    dates.sort(lambda a,b:a.compareTo(b))
    return map(lambda d: dateFormat.format(d).upper(), dates)

def buildInflowHydrograph(subbasinName):
    """Find all the FLOW files for the given subbasin, then concatenate their values together in chronological order"""
    inflowHydrographValues = []

    for date in flowFileDates(config.hmsRunName):
        subbasinDataPath = "//" + subbasinName + "/FLOW/" + date + "/" + config.interval + "/RUN:" + config.hmsRunName + "/"
        # inflowHydrographValues = dss.get(subbasinDataPath.upper().values, True) #should retrieve from all dates
        #print(dss.get(subbasinDataPath.upper()).values)
        inflowHydrographValues.extend( dss.get(subbasinDataPath.upper()).values )

    # is this really necessary?
    class ConsolidatedHydrograph:
        def __init__(self):
            self.values = inflowHydrographValues

    return ConsolidatedHydrograph();

def buildStorageOutflowCurve(subbasinName, subBasinArea, allowableReleaseRatePerAcre, intervalNum):
    consolidatedHydrograph = buildInflowHydrograph(subbasinName)
    #subbasinDataPath = "//" + subbasinName + "/FLOW/" + startDate + "/5MIN/RUN:" + config.hmsRunName + "/"
    #consolidatedHydrograph = dss.get(subbasinDataPath.upper(), True).values #should retrieve from all dates
    return buildStorageOutflowCurveFromHydrograph(consolidatedHydrograph, subBasinArea, allowableReleaseRatePerAcre, intervalNum)

def findInflowStart(hydrograph, subBasinArea):
    """Find the index into the hydrograph where the flow rises above the 3% threshold"""
    maxValueIdx, maxValue = indexOfMaxValue(hydrograph)
    # We consider the start of the inflow to be the point where the flow is above 3% of
    # the maximum release rate under consideration (0.3 cfs/ac).
    maximumOverallReleaseRate = 0.3 * subBasinArea # cfs
    inflowStartThreshold = 0.03 * maximumOverallReleaseRate
    inflowStartIndex = findFirst(hydrograph.values, lambda x : x > inflowStartThreshold)
    assert(inflowStartIndex < maxValueIdx)
    return inflowStartIndex

def findMaxReleaseRateIndex(hydrograph, allowableReleaseRate):
    """Find the index into the hydrograph where the inflow rate drops below allowable release rate"""
    maxValueIdx, maxValue = indexOfMaxValue(hydrograph)
    # The maximum release rate is the point where the inflow rate drops below the allowable release rate.
    # We search backwards through the hydrograph to ensure we find the *last* point where this occurs.
    # Searching forward would simply return the first value in the hydrograph.
    #print(maxValueIdx, len(hydrograph.values), maxValue)
    #maxReleaseRateIndex = findFirstAfterPeak(maxValueIdx, hydrograph.values, lambda x : x < allowableReleaseRate )
    maxReleaseRateIndex = findLast(hydrograph.values, lambda x : x > allowableReleaseRate )
    assert(maxReleaseRateIndex > maxValueIdx)
    return maxReleaseRateIndex

def buildStorageOutflowCurveFromHydrograph(inflowHydrograph, subBasinArea, allowableReleaseRatePerAcre, intervalNum):
    print("Building Storage-Outflow curve from hydrograph...")
    allowableReleaseRate = allowableReleaseRatePerAcre * subBasinArea # cfs
    maxValueIdx, maxValue = indexOfMaxValue(inflowHydrograph)
    if maxValue > allowableReleaseRate:
        inflowStartIndex = findInflowStart(inflowHydrograph, subBasinArea)
        maxReleaseRateIndex = findMaxReleaseRateIndex(inflowHydrograph, allowableReleaseRate)

        outflowCurveTimeSteps = maxReleaseRateIndex - inflowStartIndex + 1
        outflowRates = [] # cfs
        timeStep = intervalNum * 60 # seconds

        # The storage accumulation is performed over the entire inflow curve, not just the period
        # after it passes inflowStartThreshold. This means that the initial value in the cumulative
        # storage array is actually the sum of (inflow * timeStep) up to the point where the
        # inflow rate crosses inflowStartThreshold.
        initialCumulativeStorage = timeStep * sum(inflowHydrograph.values[:inflowStartIndex-1])
        cumulativeStorage = [initialCumulativeStorage] # cubic feet

        for i in range(0, outflowCurveTimeSteps + 1):
            x = i/float(outflowCurveTimeSteps)
            outflowRate = x * allowableReleaseRate
            outflowRates.append(outflowRate)
            inflowRate = inflowHydrograph.values[inflowStartIndex + i - 1]
            storageInCurrentTimestep = (inflowRate - outflowRate) * timeStep *1.01
            #print(i, inflowRate, outflowRate, allowableReleaseRate, outflowCurveTimeSteps)

            if (i > 0) and (storageInCurrentTimestep < 0):
                # the first timestep often has no inflow and no outflow, so we
                # only perform this assertion in later timesteps
                # this ensures that the storage is always increasing; HEC-HMS throws an error if it isn't
                #print(i, outflowCurveTimeSteps, inflowRate, outflowRate, storageInCurrentTimestep)
                #assert(storageInCurrentTimestep > 0)
                storageInCurrentTimestep = 0.0001

            cumulativeStorage.append(cumulativeStorage[i] + storageInCurrentTimestep)

        # convert the cumulative storage array to acre-ft by dividing by the number of
        # sq ft in an acre. We also ignore the initial cumulative storage value as this
        # value is only used to initialize the cumulative storage calculation.
        cumulativeStorage_acreft = map(lambda x: x/43560, cumulativeStorage[1:])
    else:
        outflowRates = [0.0, 10000.0, 100000.0, 1000000.0]
        cumulativeStorage_acreft = [0.0, 0.01, 0.10, 0.50]

    return outflowRates, cumulativeStorage_acreft

# NOTE: this function assumes the table is already in the DSS file (as outlined
# in step 6 of the example workflow)
def writeTable(tableName, storage, outflowRates):
    """Write a storage curve to the DSS file"""
    print("Writing new storage-outflow curve " + tableName)
    storageOutflowCurve = dss.get(tableName)
    storageOutflowCurve.xOrdinates = storage
    storageOutflowCurve.yOrdinates = [outflowRates]
    storageOutflowCurve.numberOrdinates = len(storage)
    dss.put(storageOutflowCurve)

def recordTotalStorage(storage, subbasin, totStorage):
    totStorage[subbasin] = storage[-1]
    return totStorage

def writeTotalStorage(totStorage, fileName, filePath):
    csvfile = open(filePath + fileName + "_storage.csv", 'wb')
    for k in totStorage.keys():
        csvfile.write(k + ", " + str(totStorage[k]) + "\n")
    csvfile.close()

# obtain configuration details for HEC applications for
# python and jython scripts
import hecConfig
config = hecConfig.HecConfig()
#pprint(vars(config))
dssFilePath = config.dssfile #config.getHmsProjectPath() + "/" + config.hmsProjectName + ".dss"
dss = HecDss.open(dssFilePath)
print("Output DSS file is " + dssFilePath)

# Read the subbasin information from the pickle file saved by the calling script (hecModel.py)
import pickle
dtf = open(config.getDataTransferFilePath(),'r+')
subbasins = pickle.load(dtf)
dtf.close()

acresPerSqMile = 640
intervalNum = config.intervalNum
print("Time step is " + str(intervalNum) + " minutes")
totStorage = {}

# Build and save the outflow-storage curve for each sub basin
for subbasin in subbasins:
    if not subbasin['tableName'] == '':
        #print(subbasin['area'])
        outflowRates, storage = buildStorageOutflowCurve(subbasin['name'], subbasin['area'] * acresPerSqMile, subbasin['releaseRate'], intervalNum)
        totStorage = recordTotalStorage(storage, subbasin['name'], totStorage)
        writeTable("//"+ subbasin['tableName'] + "/STORAGE-FLOW///TABLE/", storage, outflowRates)
writeTotalStorage(totStorage, config.hmsProjectName, config.modelVersion)

dss.done()
