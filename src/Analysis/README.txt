### Analyzing HEC-HMS and HEC-RAS output: part of the AutoHEC package ###
Code repository for automation scripts related to the Metropolitan Water
Reclamation District of Greater Chicago Watershed Release Rate project
at the Illinois State Water Survey (2015-2016).
  *Developed using Python 2.7.11, HEC-HMS 3.5, HEC-RAS 4.0, and HEC-DSSVue 2.0.1
  *Creator(s): Nicole JS Gaynor, ISWS
  *User instrutions in AutoHEC/src/Analysis/USER_HOW-TO.txt


## Structure of Inundation code ##
# runHEC_Inundation.cmd #
**may need to modify python path**
--description: Windows command line script that runs HEC_Inundation.py;
  outputs to HEC_Inundation_out.txt
--depends on: HEC_Inundation.py

# HEC_Inundation.py [driver script] #
**can be run independently or from Compare_Inundation.py--may comment
or uncomment the method call**
--description: automatically extracts data from DSS file based on
  BankStationConfig.py settings and calculates the max out-of-banks
  level and number of time periods out of banks for each event at each
  real cross section on the stream in HEC-RAS
--depends on: getStageData.py, HEC_Inundation_Config.py
--getData: runs getStageData.py, which retrieves data from DSS file
  created in HEC-RAS
--roundSigfigs(num, sigfigs): rounds num to sigfigs number of significant
  figures; for river stations, sigfigs is seven because only eight
  characters are allowed
--getTimeStage(dataPath): read time series of stage data for each river
  station from timestage.txt, created in getStageData.py; filter out
  interpolated or structure-related stations and store in a dictionary
  {river/reach/station:[time series of stage]}
--getBankElevations(bankFile): reads elevation of left and right bank
  stations from CSV file and stores in dictionary similar to timestage;
  CSV is derived from HEC-RAS GUI output
--getMaxStage(timestage, dataPath): read maxstage data for each river
  station from maxstage.txt, created in getStageData.py; filter out
  interpolated or structure-related stations using timestage as the
  reference standard; store in a dictionary {river/reach/station:maxstage}
--checkInputs(bank, timestage, maxstage): checks that maxstage, bank, and
  timestage include the same keys (river/reach/station) and are the same
  length; it should be impossible for one of these to be true while the
  other is false
--match_stations(config): runs methods that filter out interpolated and
  structure-related stations and makes sure all datasets have same stations
--getStationID(item): splits up river/reach and stationID
--OOB_DepthTime(bank, timestage, maxstage): calculates the max out-of-banks
  depth using maxstage and the length of time (number of time steps) out of
  banks using timestage; stores both in a list
--writeOOB_DepthTime(outFile, overflow): writes list of OOB depth and duration
  to a CSV file
--main: drives the workflow of the entire program and prints the length of all
  three main datasets for one last check

# getStageData.py #
**may need to modify path to getStageData.py in line 2**
--description: Jython script that runs using HEC-DSSVue.cmd; retrieves
  data from DSS file for use in HEC_Inundation.py
--depends on: HEC_Inundation_Config.py


## Structure of Compare_peakTimeElev.py ##
--getData(): calls getPeakData.py, which extracts the max stage
  and the time of the max stage for each station
--roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
  figures; for river stations, sigfigs is seven because only eight
  characters are allowed
--readFromFile(filePath, fileName): reads data from pickled file created using
  getPeakData.py
--findDiff(baseData, compareData, dataType): calculates the difference in max stage
  depth and time between two model versions. The color of the plotted point . Any depth
  differences >0.1 ft can be printed in the output with the station ID.
--reassignKeys(dataDict): the original keys are the complete data address in the
  DSS file. This changes it to only include the river, reach, and station ID
  separated by spaces (no forward slash).
--getPeak(versions, filePath): drives the looping process through
  each model version, calling other methods
--plotScatter(dataX, dataY, versions, filePath): Plots the difference between two datasets
  on a scatter plot with depth on the y-axis and time on the x-axis.


## Structure of Compare_StorageOutflow.py ##
--getData(): calls getSOData.py, which extracts the storage-outflow paired
  data for each subbasin
--roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
  figures; for river stations, sigfigs is seven because only eight
  characters are allowed
--readFromFile(filePath, fileName): reads data from a pickled file created using
  getSOData.py
--reassignKeys(dataDict): the original keys are the complete data address in the
  DSS file. This changes it to only include the river, reach, and station ID
  separated by spaces (no forward slash).
--plotLines(filePath, plotData, figName, versions): Plots the storage-outflow
  curves in multiple datasets on a single axis for comparison
--getSO(versions, filePath): driver method that reads data from text files
  created using getSOData.py, matches subbasins, and calls plotSO to plot
  specified storage-outflow curves


## Structure of Compare_hydrographs.py ##
--getData(): calls getFlowData.py, which extracts the flow data
  for each station from the RAS DSS file
--roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
  figures; for river stations, sigfigs is seven because only eight
  characters are allowed
--readFromFile(filePath, fileName): reads data from a pickled file created using
  getPeakData.py
--reassignKeys(dataDict): the original keys are the complete data address in the
  DSS file. This changes it to only include the river, reach, and station ID
  separated by spaces (no forward slash).
--plotLines(filePath, plotData, figName, versions): Plots the hydrographs in multiple
  datasets on a single axis for comparison
--getFlow(versions, filePath): reads data from text files created using getFlowData.py,
  matches stations, and calls plotLines to plot both hydrographs curves


## Structure of Compare_Inundation.py ##
--roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
  figures; for river stations, sigfigs is seven because only eight
  characters are allowed
--readFromFile(filePath, fileName): reads  data from pickled file [not used]
--readFromCSV(filePath, fileName): Reads inundation data from CSV file
--findDiff(baseData, compareData): calculates the difference in inundation
  depth and time between two model versions. If the base model version shows no out-
  of-banks depth, the difference is set to -1; if the comparison model version shows
  no out-of-banks depth, the difference is set to -2. Any depth differences >0.1 ft
  or time differences >0.5 are printed in the output with the station ID.
--getPeak(versions, filePath, savePath, watershed, timestep): drives the looping process through
  each model version, calling other methods
--plotScatter(dataX, dataY, versions, filePath, timestep): Plots the difference between two datasets
  on a scatter plot with depth on the y-axis and time on the x-axis.


## Structure of makeMaxWselCsv.py ##
--getData(): calls getPeakData.py, which extracts the max stage
  and the time of the max stage for each station
--roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
  figures; for river stations, sigfigs is seven because only eight
  characters are allowed
--readFromFile(filePath, fileName): reads data from a pickled file created using
  getPeakData.py
--reassignKeys(dataDict): the original keys are the
  complete data address in the DSS file. This changes it to only include the river, reach,
  and station ID separated by spaces (no forward slash).
--splitKey(k): splits a key into river, reach, and station ID as three separate items
--filterStations(filePath): filters the stations that are stored for output using the
  provided CSV file (currently "USC_MEEKMA_CSV.csv")
--removePeriod(versions): replaces the decimal in a version number with an underscore,
  hopefully allowing direct import into GIS software
--writeToCSV(writeData, filePath, versions): writes max stage from all versions listed
  in Compare_Config.py to a CSV file, along with the river, reach, and station IDs as
  filtered using filterStations. CSV file includes a header row.
--getPeak(versions, filePath, runName): driver method that reads in, processes, and
  writes max stage data to a CSV file.