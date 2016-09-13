### AutoHEC ###
Code repository for automation scripts related to the Metropolitan Water
Reclamation District of Greater Chicago Watershed Release Rate project
at the Illinois State Water Survey (2015-2016).
  *Developed using Python 2.7.11, HEC-HMS 3.5, HEC-RAS 4.0, and HEC-DSSVue 2.0.1
  *Creator(s): Optimatics (optimatics.com); Nicole JS Gaynor, ISWS
  *User instructions in AutoHEC/src/USER_HOW-TO.txt


## System requirements ##
**This package only runs on Windows operating systems.**
--Python 2.7.11 (code has not been tested with any other version)
--Python for Windows [Extensions](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download) x86 v219 (required for COM manipulation).
--HEC-DSSVue downloaded to the src/ directory; it does not need to
  be installed.
--HEC-HMS and HEC-RAS must be installed on the system. The location
  of HEC-HMS can be set in the parent_hecConfig_*.py configuration
  file using self.hmsDir.


## Known issues ##
No known issues with this code. (7/8/2016)
**A warning about using the HEC-RAS model: Do NOT edit the HTAB parameter
in the HEC-RAS GUI. It causes a Fortran error in the model code itself.
If you do and you get a Fortran error, replace the geometry file with
the original version (which I hope you saved from a prior model setup).**


## Structure of automation code from Optimatics (as modified by NJS Gaynor) ##
# runModel.cmd #
** You must choose the input text file that lists the names of the config files.
   Use two colons to comment out all the options you do *not* wish to use. **
--description: sets environmental variables and initiates python scripts; command-
  line input should be text file that contains the prefixes for each hecConfig.py
  file
--depends on: runModel.py

# *_hecConfig.py (class HecConfig imported as config) #
--description: config file with setup variables for HMS and RAS runs;
  these files are copied to hecConfig.py for use in the program and the
  original files are retained. There are different parent_hecConfig files for
  each model location.
--getDataTransferFilePath: returns path to a temporary file that stores pickled
  data for use later in the program
--getHmsProjectPath: path to HMS project files
--getRasProjectPath: path to RAS project files

# runModel.py #
--description: controls workflow that splits basins and runs HEC-HMS and HEC-RAS;
  reads lines from input file to find config file for each subsubwatershed, if needed
--depends on: hecModel.py, *hecConfig.py

# hecModel.py (class Model) #
--description: contains all methods to control automation of HEC-HMS and HEC-RAS
--depends on: RunHecHmsModel.py, createStorageOutflowCurves.py,
  ExampleHydraulicComparison.py, win32com module
--runHms: runs HMS model using HEC-HMS.cmd
--newStorageOutflowCurves: creates new storage-outflow curves in the DSS file with dummy
  data for use with the new Reservoirs
--createStorageOutflowCurves(subbasins): modifies the storage-outflow curve data based on
  Amanda Flegel's algorithm
--runRas: runs HEC-RAS using HECRASController
--getHydraulicResults(ditchNames) [not currently used]: retrieves and processes RAS results
  from DSS file using ExampleHydraulicComparison.py and ExampleDssUsage.py

# runHecHmsModel.py #
--description: runs HEC-HMS instance using hms python module; exactly as in HEC-HMS
  documentation for command line use of the model
--depends on: hecConfig.py, hms module

# dummyStorageOutflowCurves.py (added by NJS Gaynor) #
--description: creates dummy storage outflow curves using HEC-DSSVue jython script and inserts
  table into DSS file for use with new Reservoirs added in InitHMS.py
--depends on: hec module, *hecConfig.py, ExampleHydraulicComparison.py (by way of dtf file)

# copyStorageOutflowCurves.py (added by NJS Gaynor) #
--description: copies storage outflow curves from a HEC-HMS DSS file that used 24h precip
  and pastes the curves into the corresponding run that uses 12h precip, using HEC-DSSVue
  jython script, for use with new Reservoirs added in InitHMS.py
--depends on: hec module, *hecConfig.py, ExampleHydraulicComparison.py (by way of dtf file)

# createStorageOutflowCurves.py #
--description: replaces the dummy storage-outflow curve created in dummyStorageOutflowCurves.py
  because this method assumes the table exists; initial storage is the accumulation of the inflow
  until the inflow exceeds 3% of the allowable release rate for the subbasin (based on subbasin
  size and a 0.3 cfs/acre release rate); then outflow hydrograph is a straight line
  from that point to the point at which inflow drops below the max allowable release rate. For
  any times where the hydrograph dips below the rating curve, the storage for that time step is
  set to zero (would otherwise be negative) in order to avoid model errors. Also, some subbasins
  do not require detention; in that case the rating curve is assigned such that the reservoir
  is free flowing. The entire rating curve is multiplied by 1.01 to avoid rounding errors, which
  cause more reservoirs to overflow during the second HEC-HMS run.
--depends on: hec module, *hecConfig.py, ExampleHydraulicComparison.py (by way of dtf file)
--indexOfMaxValue(hydrograph): finds the index of the maximum value in the inflow hydrograph
--findFirst(sequence, predicate): find the first element in which predicate is true
--findLast(sequence, predicate): find the last element in which predicate is true
--any(predicate, container): returns true if predicate is true in any element of the container
--flowFileDates: finds all dates for FLOW files in the DSS catalog give specified model run;
  will not be accurate if there is more than one set of data for the specified model run (i.e.
  more than one distinct time period)
--buildInflowHydrograph(subbasinName)[calls flowFileDates]: retrieves the FLOW data from the RAS DSS file and
  concatenates it into a single time series
--buildStorageOutflowCurve(subbasinName, subBasinArea, allowableReleaseRatePerAcre) [calls
  buildInflowHydrograph, buildStorageOutflowCurveFromHydrograph]: returns values from
  buildStorageOutflowCurveFromHydrograph
--findInflowStart(hydrograph, subBasinArea) [calls indexOfMaxValue, findFirst]: finds the
  beginning of the outflow hydrograph (i.e. where the inflow hydrograph exceeds 3% of the
  max allowable release rate for the subbasin based on 0.3 cfs/acre)
--findMaxReleaseRateIndex(hydrograph, allowableReleaseRate) [calls indexOfMaxValue, findLast]:
  finds the end of the outflow hydrograph (i.e. where the inflow drops below the max
  allowable release rate for the subbasin based on 0.3 cfs/acre)
--buildStorageOutflowCurveFromHydrograph(inflowHydrograph, SubBasinArea, allowableReleaseRatePerAcre)
  [calls findInflowStart, findMaxReleaseRateIndex]: calculates each time step of the straight-line
  outflow hydrograph from the index found in findInflowStart to the index found in
  findMaxReleaseRateIndex and calculates the accumulated storage over this period
--writeTable(tableName, storage, outflowRates): writes new storage-outflow table to the RAS
  DSS file
--recordTotalStorage(storage, subbasin, totStorage): records the max storage from each storage-outflow
  curve
--writeTotalStorage(totStorage, fileName, filePath): writes total storage for each subbasin to a
  CSV file named *_storage.csv stored in the model version directory

# ExampleDssUsage.py #
--description: shows how to access (read/write) data to DSS file
--depends on: hec module, *hecConfig.py
--GetMaxValueIndex(hydrograph): finds index of the maximum value in hydrograph

# ExampleHydraulicComparison.py #
--description: retrieves hydraulic results from DSS file (does nothing with them yet)
--depends on: hec module, *hecConfig.py
--GetMaxValueIndex(hydrograph): finds index of the maximum value in hydrograph
