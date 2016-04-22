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
    print("getting dates from ", hmsRunName)

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

def buildStorageOutflowCurve(subbasinName, subBasinArea, allowableReleaseRatePerAcre):
    consolidatedHydrograph = buildInflowHydrograph(subbasinName)
    #subbasinDataPath = "//" + subbasinName + "/FLOW/" + startDate + "/5MIN/RUN:" + config.hmsRunName + "/"
    #consolidatedHydrograph = dss.get(subbasinDataPath.upper(), True).values #should retrieve from all dates
    return buildStorageOutflowCurveFromHydrograph(consolidatedHydrograph, subBasinArea, allowableReleaseRatePerAcre)

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

def buildStorageOutflowCurveFromHydrograph(inflowHydrograph, subBasinArea, allowableReleaseRatePerAcre):
    allowableReleaseRate = allowableReleaseRatePerAcre * subBasinArea # cfs
    maxValueIdx, maxValue = indexOfMaxValue(inflowHydrograph)
    if maxValue > allowableReleaseRate:
        inflowStartIndex = findInflowStart(inflowHydrograph, subBasinArea)
        maxReleaseRateIndex = findMaxReleaseRateIndex(inflowHydrograph, allowableReleaseRate)

        outflowCurveTimeSteps = maxReleaseRateIndex - inflowStartIndex + 1
        outflowRates = [] # cfs
        timeStep = 6*60 # seconds

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
    storageOutflowCurve = dss.get(tableName)
    storageOutflowCurve.xOrdinates = storage
    storageOutflowCurve.yOrdinates = [outflowRates]
    storageOutflowCurve.numberOrdinates = len(storage)
    dss.put(storageOutflowCurve)

# Test the curve building function against all the curves in the Lucas Ditch HMS model:
# buildStorageOutflowCurve("W146260", 10, 0.15)
# buildStorageOutflowCurve("W146370", 10, 0.15)
# buildStorageOutflowCurve("W146380", 10, 0.15)
# buildStorageOutflowCurve("W146470", 10, 0.15)
# buildStorageOutflowCurve("W146480", 10, 0.15)
# buildStorageOutflowCurve("W146520", 10, 0.15)
# buildStorageOutflowCurve("W146540", 10, 0.15)
# buildStorageOutflowCurve("W146580", 10, 0.15)
# buildStorageOutflowCurve("W146590", 10, 0.15)
# buildStorageOutflowCurve("W146630", 10, 0.15)
# buildStorageOutflowCurve("W146690", 10, 0.15)
# buildStorageOutflowCurve("W146790", 10, 0.15)
# buildStorageOutflowCurve("W146830", 10, 0.15)
# buildStorageOutflowCurve("W146880", 10, 0.15)

# obtain configuration details for HEC applications for
# python and jython scripts
import hecConfig
reload(hecConfig)
config = hecConfig.HecConfig()
dssFilePath=config.getHmsProjectPath() + "/" + config.hmsProjectName + ".dss"
dss = HecDss.open(dssFilePath)

# Test the curve building function against the data from the 'StorageOutflowRatingCurveCalculationv2.xlsx'
# spreadsheet:

# class TestHydrograph:
#     def __init__(self):
#         self.values = [
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.001, 0.004, 0.011, 0.025, 0.048, 0.077, 0.111, 0.145, 0.175,
#          0.201, 0.223, 0.241, 0.257, 0.271, 0.286, 0.302, 0.318, 0.335, 0.351, 0.37, 0.392, 0.419, 0.455, 0.498, 0.545,
#          0.595, 0.644, 0.692, 0.737, 0.778, 0.816, 0.852, 0.885, 0.918, 0.948, 0.977, 1.006, 1.033, 1.059, 1.084, 1.109,
#          1.133, 1.156, 1.179, 1.2, 1.222, 1.243, 1.263, 1.283, 1.302, 1.321, 1.339, 1.357, 1.374, 1.391, 1.408, 1.424,
#          1.44, 1.456, 1.471, 1.486, 1.5, 1.518, 1.542, 1.577, 1.627, 1.691, 1.764, 1.84, 1.913, 1.981, 2.042, 2.092,
#          2.135, 2.173, 2.206, 2.239, 2.281, 2.342, 2.433, 2.557, 2.704, 2.863, 3.02, 3.166, 3.297, 3.408, 3.499, 3.575,
#          3.64, 3.696, 3.76, 3.846, 3.973, 4.156, 4.386, 4.642, 4.901, 5.146, 5.367, 5.557, 5.71, 5.835, 5.94, 6.03, 6.12,
#          6.232, 6.39, 6.619, 6.921, 7.271, 7.636, 7.99, 8.315, 8.598, 8.83, 9.016, 9.168, 9.295, 9.405, 9.504, 9.601,
#          9.707, 9.827, 9.956, 10.089, 10.216, 10.335, 10.44, 10.53, 10.605, 10.667, 10.721, 10.768, 10.791, 10.769,
#          10.679, 10.496, 10.229, 9.912, 9.581, 9.264, 8.981, 8.742, 8.559, 8.422, 8.316, 8.234, 8.163, 8.085, 7.977,
#          7.818, 7.601, 7.341, 7.067, 6.8, 6.557, 6.347, 6.179, 6.053, 5.955, 5.879, 5.819, 5.761, 5.692, 5.595, 5.458,
#          5.287, 5.099, 4.912, 4.738, 4.585, 4.458, 4.363, 4.29, 4.233, 4.188, 4.145, 4.093, 4.016, 3.901, 3.747, 3.567,
#          3.38, 3.201, 3.039, 2.901, 2.793, 2.71, 2.646, 2.595, 2.554, 2.515, 2.47, 2.412, 2.335, 2.244, 2.146, 2.051,
#          1.963, 1.887, 1.825, 1.778, 1.742, 1.713, 1.691, 1.673, 1.659, 1.649, 1.64, 1.634, 1.629, 1.626, 1.623, 1.621,
#          1.619, 1.617, 1.616, 1.616, 1.615, 1.615, 1.614, 1.614, 1.614, 1.614, 1.614, 1.614, 1.614, 1.615, 1.615, 1.615,
#          1.615, 1.615, 1.615, 1.615, 1.604, 1.57, 1.501, 1.383, 1.226, 1.048, 0.868, 0.7, 0.551, 0.427, 0.333, 0.261,
#          0.205, 0.161, 0.125, 0.098, 0.076, 0.059, 0.046, 0.036, 0.028, 0.021, 0.016, 0.013, 0.009, 0.007, 0.005, 0.003,
#          0.002, 0.001, 0.001, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#
#         # Time values don't need to match those found in the spreadsheet, as long as the timestep is 5 minutes
#         # the calculations are still correct.
#         self.times = map( lambda x: x*5, range(0,len(self.values)))
#
# spreadsheetHydrograph = TestHydrograph()
#
# outflowRates, storage = (buildStorageOutflowCurveFromHydrograph(spreadsheetHydrograph, 13.2224, 0.15))
# writeTable("//TABLE 1/STORAGE-FLOW///TABLE/", storage, outflowRates)
#
# outflowRates, storage = (buildStorageOutflowCurveFromHydrograph(spreadsheetHydrograph, 13.2224, 0.20))
# writeTable("//TABLE 2/STORAGE-FLOW///TABLE/", storage, outflowRates)
#
# outflowRates, storage = (buildStorageOutflowCurveFromHydrograph(spreadsheetHydrograph, 13.2224, 0.25))
# writeTable("//TABLE 3/STORAGE-FLOW///TABLE/", storage, outflowRates)
#
# outflowRates, storage = (buildStorageOutflowCurveFromHydrograph(spreadsheetHydrograph, 13.2224, 0.30))
# writeTable("//TABLE 4/STORAGE-FLOW///TABLE/", storage, outflowRates)

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
        outflowRates, storage = buildStorageOutflowCurve(subbasin['name'], subbasin['area'] * acresPerSqMile, subbasin['releaseRate'])
        writeTable("//"+ subbasin['tableName'] + "/STORAGE-FLOW///TABLE/", storage, outflowRates)

dss.done()
