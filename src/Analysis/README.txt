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
--writePeakDiff(outFile, flowDiff): Writes flowDiff to outFile [not currently used]
--getPeak(bVersions, cVersions, filePath, runName): reads data from
  text files created using getPeakData.py, matches stations, and finds the difference
  in the max stage time and elevation between the model versions in the config file;
  also lists any elevation differences greater than 0.1 ft and time differences greater
  than 0.5 hours. Calls plotScatter, which creates a scatter plot of the differences
  in time and elevation between the model versions.
--plotScatter(dataManualX, dataManualY, dataAutoX, dataAutoY,
  dataDiffX, dataDiffY, bV, cV, filePath): Plots the difference between two datasets on a
  scatter plot with max stage elevation on the y-axis and max stage time on the x-axis.


## Structure of Compare_StorageOutflow.py ##
--getData(): calls getSOData.py, which extracts the storage-outflow paired
  data for each subbasin
--roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
  figures; for river stations, sigfigs is seven because only eight
  characters are allowed
--writePeakDiff(outFile, flowDiff): Writes flowDiff to outFile [not currently used]
--getSO(bVersions, cVersions, filePath): reads data from
  text files created using getSOData.py, matches subbasins, and calls plotSO to plot both
  storage-outflow curves
--plotSO(soDataManual, soDataAuto, tableName, filePath, bV, cV): Plots the
  storage-outflow curves in two datasets on a single axis for comparison


## Structure of Compare_hydrographs.py ##
--getData(): calls getFlowData.py, which extracts the flow data
  for each station from the RAS DSS file
--roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
  figures; for river stations, sigfigs is seven because only eight
  characters are allowed
--writeFlowDiff(outFile, flowDiff): Writes flowDiff to outFile [not currently used]
--getFlow(bVersions, cVersions, filePath): reads data from
  text files created using getFlowData.py, matches stations, and calls plotFlow to plot both
  hydrographs curves
--plotFlow(soDataManual, soDataAuto, figName, bV, cV, filePath): Plots the
  hydrographs in two datasets on a single axis for comparison
