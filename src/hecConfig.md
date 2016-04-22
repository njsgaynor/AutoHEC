By *.py file:
copyStorageOutflowCurves: getHmsProjectPath (path to HMS files), hmsProjectName (HMS DSS file name),
getDataTransferFilePath

createStorageOutflowCurves: getHmsProjectPath, hmsProjectName, getDataTransferFilePath

dummyStorageOutflowCurves: getHmsProjectPath, hmsProjectName, getDataTransferFilePath

ExampleDssUsage: getHmsProjectPath, hmsProjectName, hmsRunName (for data address in DSS file)

ExampleHydraulicComparison: getRasProjectPath (location of RAS DSS file), rasProjectName (RAS DSS file name), 
getDataTransferFilePath, rasPlanName (data address)

hecModel: hmsDir, hmsCommand, scriptPath, dssDir (DSSVue directory), getDataTransferFilePath, dssCommand, 
getRasProjectPath, rasProjectName

RunHecHmsModel: hmsProjectName, getHmsProjectPath, hmsRunName (from compute tab in HMS, used to run HMS model)

runModel: scriptPath, inputFileName (created in InitHMS), hmsRunName

InitHMS: scriptPath, stationFileName, inputFileName, hmsGageName (to set gages in MET file), hmsMetFile, 
getHmsProjectPath

Subwatershed_class: basinsin, basinout, pdatafile, dssfile, redevelopment, curvenumber, releaserate


By config param:
scriptPath: hecModel, runModel, InitHMS
hmsDir: hecModel
modelPath: [internal use]
modelVersion: [internal use]
hmsVersion: [internal use]
hmsCommand: hecModel
dssDir: hecModel
dssCommand: hecModel
osModelVersion: [internal use]
osHmsVersion: [internal use]
hmsRunName: ExampleDssUsage, RunHecHmsModel, runModel
hmsMetFile: InitHMS
hmsGageName: InitHMS
redevelopment, curvenumber, releaserate: Subwatershed_class
numHmsModels: [not explicitly used]
basinin, basinout, pdatafile, dssfile: Subwatershed_class
osDssFile: copyStorageOutflowCurves
inputFileName: runModel, InitHMS
rasProjectName: ExampleHydraulicComparison, hecModel
rasPlanName: ExampleHydraulicComparison
rasProjectPath: ExampleHydraulicComparison, hecModel
stationFileName: InitHMS
hmsProjectPath: copyStorageOutflowCurves, createStorageOutflowCurves, dummyStorageOutflowCurves, 
ExampleDssUsage, RunHecHmsModel, InitHMS
osHmsProjectPath: copyStorageOutflowCurves
hmsProjectName: copyStorageOutflowCurves, createStorageOutflowCurves, dummyStorageOutflowCurves, 
ExampleDssUsage, RunHecHmsModel
