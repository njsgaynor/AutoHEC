<h1>Analyzing HEC-HMS and HEC-RAS output: part of the AutoHEC package</h1>
<p>Code repository for automation scripts related to the Metropolitan Water
Reclamation District of Greater Chicago Watershed Release Rate project
at the Illinois State Water Survey (2015-2016).<br />
<em>&nbsp;&nbsp;&nbsp;&nbsp;Developed using Python 2.7.11, HEC-HMS 3.5, HEC-RAS 4.0,and 
HEC-DSSVue 2.0.1</em><br />
<em>&nbsp;&nbsp;&nbsp;&nbsp;Creators: Nicole JS Gaynor, ISWS</em></p>


<h4>Purpose</h4>
<p>The Compare_*.py scripts were developed to compare two model versions of HEC-HMS 
and HEC-RAS. It is used both to test the automation code in AutoHEC against
a manual version of the same model run and to compare multiple automated 
versions of the model (with different release rates, redevelopment rates, 
etc.) to assess the effect of each of these factors.</p>

<p>HEC_Inundation.py is somewhat different in that it uses a single model 
run and calculates the duration and max depth of water over the lower bank 
station at each river station. It is currently not set up to compare model 
automatically. Data is output into a CSV file for easy processing elsewhere 
or viewing in Excel.<p>


<h4>How to run code that calculates time and depth of inundation</h4>
<p><ol><li>Modify HEC_Inundation_Config.py to find the files and data addresses
for the stage time series, max stage elevation, and max stage time. 
<strong>When preparing the bank station elevations file, do not include 
Node Names in the table (under Options menu in the Profile Output 
Table of HEC-RAS).</strong>
</li><li>Open Windows Command Prompt.
</li><li>Change to directory containing runInitHMS.cmd (AutoHEC/src/WeRunFirst) 
directory ("dir" lists directory contents and "cd" changes directory).
</li><li>Type "runHEC_Inundation.cmd" into the Windows command line and press Enter.
Output will be saved to HEC_Inundation_output.txt.</li></ol></p>


<h4>Structure of Inundation code</h4>
<h6>runHEC_Inundation.cmd</h6>
<p><ul><li><strong>may need to modify python path</strong>
</li><li>description: Windows command line script that runs HEC_Inundation.py;
outputs to HEC_Inundation_out.txt
</li><li>depends on: HEC_Inundation.py</li></ul></p>

<h6>HEC_Inundation.py [driver script]</h6>
<p><ul><li>description: automatically extracts data from DSS file based on 
BankStationConfig.py settings and calculates the max out-of-banks
level and number of time periods out of banks for each event at each
real cross section on the stream in HEC-RAS
</li><li>depends on: getStageData.py, HEC_Inundation_Config.py
</li><li>getData: runs getStageData.py, which retrieves data from DSS file 
created in HEC-RAS
</li><li>roundSigfigs(num, sigfigs): rounds num to sigfigs number of significant
figures; for river stations, sigfigs is seven because only eight 
characters are allowed
</li><li>getTimeStage(dataPath): read time series of stage data for each river
station from timestage.txt, created in getStageData.py; filter out
interpolated or structure-related stations and store in a dictionary
{river/reach/station:[time series of stage]}
</li><li>getBankElevations(bankFile): reads elevation of left and right bank
stations from CSV file and stores in dictionary similar to timestage;
CSV is derived from HEC-RAS GUI output
</li><li>getMaxStage(timestage, dataPath): read maxstage data for each river
station from maxstage.txt, created in getStageData.py; filter out
interpolated or structure-related stations using timestage as the 
 reference standard; store in a dictionary {river/reach/station:maxstage}
</li><li>checkInputs(bank, timestage, maxstage): checks that maxstage, bank, and
timestage include the same keys (river/reach/station) and are the same
length; it should be impossible for one of these to be true while the 
other is false
</li><li>match_stations(config): runs methods that filter out interpolated and
structure-related stations and makes sure all datasets have same stations
</li><li>getStationID(item): splits up river/reach and stationID
</li><li>OOB_DepthTime(bank, timestage, maxstage): calculates the max out-of-banks
depth using maxstage and the length of time (number of time steps) out of
banks using timestage; stores both in a list
</li><li>writeOOB_DepthTime(outFile, overflow): writes list of OOB depth and duration
to a CSV file
</li><li>main: drives the workflow of the entire program and prints the length of all
three main datasets for one last check</li></ul></p>

<h6>getStageData.py</h6>
<p><strong>may need to modify path to getStageData.py in line 2</strong>
<ul><li>description: Jython script that runs using HEC-DSSVue.cmd; retrieves
data from DSS file for use in HEC_Inundation.py
</li><li>depends on: HEC_Inundation_Config.py</li></ul></p>


<h4>Structure of Compare_peakTimeElev.py</h4>
<p><ul><li>getData(): calls getPeakData.py, which extracts the max stage
and the time of the max stage for each station
</li><li>roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
figures; for river stations, sigfigs is seven because only eight 
characters are allowed
</li><li>writePeakDiff(outFile, flowDiff): Writes flowDiff to outFile [not currently used]
</li><li>getPeak(bVersions, cVersions, filePath, runName): reads data from
text files created using getPeakData.py, matches stations, and finds the difference
in the max stage time and elevation between the model versions in the config file; 
also lists any elevation differences greater than 0.1 ft and time differences greater
than 0.5 hours. Calls plotScatter, which creates a scatter plot of the differences
in time and elevation between the model versions.
</li><li>plotScatter(dataManualX, dataManualY, dataAutoX, dataAutoY, 
dataDiffX, dataDiffY, bV, cV, filePath): Plots the difference between two datasets on a
scatter plot with max stage elevation on the y-axis and max stage time on the x-axis.</li></ul></p>


<h4>Structure of Compare_StorageOutflow.py</h4>
<p><ul><li>getData(): calls getSOData.py, which extracts the storage-outflow paired
data for each subbasin
</li><li>roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
figures; for river stations, sigfigs is seven because only eight 
characters are allowed
</li><li>writePeakDiff(outFile, flowDiff): Writes flowDiff to outFile [not currently used]
</li><li>getSO(bVersions, cVersions, filePath): reads data from
text files created using getSOData.py, matches subbasins, and calls plotSO to plot both 
storage-outflow curves
</li><li>plotSO(soDataManual, soDataAuto, tableName, filePath, bV, cV): Plots the 
storage-outflow curves in two datasets on a single axis for comparison</li></ul></p>


<h4>Structure of Compare_hydrographs.py</h4>
<p><ul><li>getData(): calls getFlowData.py, which extracts the flow data
for each station from the RAS DSS file
</li><li>roundSigFigs(num, sigfigs): rounds num to sigfigs number of significant
figures; for river stations, sigfigs is seven because only eight 
characters are allowed
</li><li>writeFlowDiff(outFile, flowDiff): Writes flowDiff to outFile [not currently used]
</li><li>getFlow(bVersions, cVersions, filePath): reads data from
text files created using getFlowData.py, matches stations, and calls plotFlow to plot both 
hydrographs curves
</li><li>plotFlow(soDataManual, soDataAuto, figName, bV, cV, filePath): Plots the 
hydrographs in two datasets on a single axis for comparison</li></ul></p>
