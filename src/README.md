<h1>AutoHEC</h1>
<p>Code repository for automation scripts related to the Metropolitan Water
Reclamation District of Greater Chicago Watershed Release Rate project
at the Illinois State Water Survey (2015-2016).<br />
<em>&nbsp;&nbsp;&nbsp;&nbsp;Developed using Python 2.7.11, HEC-HMS 3.5, HEC-RAS 4.0,and 
HEC-DSSVue 2.0.1</em><br />
<em>&nbsp;&nbsp;&nbsp;&nbsp;Creators: Optimatics (optimatics.com); Nicole JS Gaynor, ISWS</em></p>

<h4>Purpose</h4>
<p>This script was built to split subbasins in to a developed and 
an undeveloped portion based on a proposed future redevelopment rate. 
Then it applies a release rate to the reservoirs in each subbasin.
The release rate is currently a single value for all subbasins in the 
automation, which can be manually edited after running InitHMS.py and 
before running HEC-HMS the second time in the *_input.json file
(inputFileName defined in the parent_hecConfig_*.py file for the
project), where * is the HMS project name. <strong>This script depends on the *.u##
file already being updated to have subbasins and reservoirs point to 
the new Junction names, which is "JN [subbasin name]".</strong></p>

<h4>Error Checking</h4>
<p>Be sure to check AutoHEC/src/output.txt to make sure that there were no
errors. Common errors may include:
<ol><li>Jython/Java error, which would appear below the blocks set off in 
colons (which indicates when the Jython interpreter starts in 
HEC-DSSVue). This may indicate a corrupted file. Try recreating the 
version directory from the source model.
</li><li>HEC-HMS error, which would be indicated after one of the HEC-HMS runs
on the line that starts with "End HEC-HMS" as "Exit status = -1". Try 
manually running HEC-HMS. The most likely problem is that a reservoir
overflowed and the max storage in the rating curve needs to be slightly 
increased (by maybe 1%).
</li><li>HEC-RAS runs in less than about 224 seconds. This will show up on the
last line of the output file. Try running the model manually in HEC-RAS.
The most likely problem is that the model becames unstable. Try using a
different time step or locating where the model becomes unstable.</li></ol></p>

<h4>Running the Scripts</h4>
<p>How to run code that splits basins and runs models**:
<ol><li>Modify *_hecConfig.py files to find the files that need to be 
modified and to reflect the characteristics of the future subbasins.
</li><li>Create a text file that lists the prefixes for the *_hecConfig.py
files needed for this HEC-RAS run. Use this file name as the input in
runModel.cmd.
</li><li>Open Windows Command Prompt.
</li><li>Change to directory containing runModel.cmd (AutoHEC/src) 
directory ("dir" lists directory contents and "cd" changes directory).
</li><li>Type "runModel.cmd" into the Windows command line and press Enter.
Output will be saved to output.txt.</li></ol>
<em>**see README in SplitBasins directory for how to run the subbasin 
splitting code on its own</em></p>

<h4>Notes</h4>
<p>[none at the moment]</p>


<h4>Structure of automation code from Optimatics (as modified by NJS Gaynor)</h4>
<h6>runModel.cmd</h6>
<p><ul><li>description: sets environmental variables and initiates python scripts; command-
line input should be text file that contains the prefixes for each hecConfig.py
file
</li><li>depends on: runModel.py</li></ul></p>

<h6>*_hecConfig.py (class HecConfig imported as config)</h6>
<p><ul><li>description: config file with setup variables for HMS and RAS runs; 
these files are copied to hecConfig.py for use in the program and the
original files are retained
</li><li>getDataTransferFilePath: returns path to a temporary file that stores pickled
data for use later in the program
</li><li>getHmsProjectPath: path to HMS project files
</li><li>getRasProjectPath: path to RAS project files</li></ul></p>

<h6>runModel.py</h6>
<p><ul><li>description: controls workflow that splits basins and runs HEC-HMS and HEC-RAS;
reads lines from input file to find config file for each subsubwatershed, if needed
</li><li>depends on: hecModel.py, *hecConfig.py</li></ul></p>

<h6>hecModel.py (class Model)</h6>
<p><ul><li>description: contains all methods to control automation of HEC-HMS and HEC-RAS
</li><li>depends on: RunHecHmsModel.py, createStorageOutflowCurves.py, 
ExampleHydraulicComparison.py, win32com module
</li><li>runHms: runs HMS model using HEC-HMS.cmd
</li><li>newStorageOutflowCurves: creates new storage-outflow curves in the DSS file with dummy
data for use with the new Reservoirs
</li><li>createStorageOutflowCurves(subbasins): modifies the storage-outflow curve data based on
Amanda Flegel's algorithm
</li><li>runRas: runs HEC-RAS using HECRASController
</li><li>getHydraulicResults(ditchNames): retrieves and processes RAS results from DSS file using 
ExampleHydraulicComparison.py and ExampleDssUsage.py</li></ul></p>

<h6>runHecHmsModel.py</h6>
<p><ul><li>description: runs HEC-HMS instance using hms python module; exactly as in HEC-HMS 
documentation for command line use of the model
</li><li>depends on: hecConfig.py, hms module</li></ul></p>

<h6>dummyStorageOutflowCurves.py (added by NJS Gaynor)</h6>
<p><ul><li>description: creates dummy storage outflow curves using HEC-DSSVue jython script and inserts
table into DSS file for use with new Reservoirs added in InitHMS.py
</li><li>depends on: hec module, *hecConfig.py, ExampleHydraulicComparison.py (by way of dtf file)</li></ul></p>

<h6>copyStorageOutflowCurves.py (added by NJS Gaynor)</h6>
<p><ul><li>description: copies storage outflow curves from a HEC-HMS DSS file that used 24h precip
and pastes the curves into the corresponding run that uses 12h precip, using HEC-DSSVue
jython script, for use with new Reservoirs added in InitHMS.py
</li><li>depends on: hec module, *hecConfig.py, ExampleHydraulicComparison.py (by way of dtf file)</li></ul></p>

<h6>createStorageOutflowCurves.py</h6>
<p><ul><li>description: replaces the dummy storage-outflow curve created in dummyStorageOutflowCurves.py
because this method assumes the table exists; initial storage is the accumulation of the inflow
until the inflow exceeds 3% of the allowable release rate for the subbasin (based on subbasin
size and a 0.3 cfs/acre release rate); then outflow hydrograph is a straight line
from that point to the point at which inflow drops below the max allowable release rate. For
any times where the hydrograph dips below the rating curve, the storage for that time step is 
set to zero (would otherwise be negative) in order to avoid model errors. Also, some subbasins
do not require detention; in that case the rating curve is assigned such that the reservoir
is free flowing. The entire rating curve is multiplied by 1.01 to avoid rounding errors, which
cause more reservoirs to overflow during the second HEC-HMS run.
</li><li>depends on: hec module, *hecConfig.py, ExampleHydraulicComparison.py (by way of dtf file)
</li><li>indexOfMaxValue(hydrograph): finds the index of the maximum value in the inflow hydrograph
</li><li>findFirst(sequence, predicate): find the first element in which predicate is true
</li><li>findLast(sequence, predicate): find the last element in which predicate is true
</li><li>any(predicate, container): returns true if predicate is true in any element of the container
</li><li>flowFileDates: finds all dates for FLOW files in the DSS catalog give specified model run; 
will not be accurate if there is more than one set of data for the specified model run (i.e.
more than one distinct time period)
</li><li>buildInflowHydrograph(subbasinName)[calls flowFileDates]: retrieves the FLOW data from the RAS DSS file and
concatenates it into a single time series
</li><li>buildStorageOutflowCurve(subbasinName, subBasinArea, allowableReleaseRatePerAcre) [calls 
buildInflowHydrograph, buildStorageOutflowCurveFromHydrograph]: returns values from 
buildStorageOutflowCurveFromHydrograph
</li><li>findInflowStart(hydrograph, subBasinArea) [calls indexOfMaxValue, findFirst]: finds the 
beginning of the outflow hydrograph (i.e. where the inflow hydrograph exceeds 3% of the 
max allowable release rate for the subbasin based on 0.3 cfs/acre)
</li><li>findMaxReleaseRateIndex(hydrograph, allowableReleaseRate) [calls indexOfMaxValue, findLast]: 
finds the end of the outflow hydrograph (i.e. where the inflow drops below the max
allowable release rate for the subbasin based on 0.3 cfs/acre)
</li><li>buildStorageOutflowCurveFromHydrograph(inflowHydrograph, SubBasinArea, allowableReleaseRatePerAcre)
[calls findInflowStart, findMaxReleaseRateIndex]: calculates each time step of the straight-line
outflow hydrograph from the index found in findInflowStart to the index found in 
findMaxReleaseRateIndex and calculates the accumulated storage over this period
</li><li>writeTable(tableName, storage, outflowRates): writes new storage-outflow table to the RAS
DSS file</li></ul></p>

<h6>ExampleDssUsage.py</h6>
<p><ul><li>description: shows how to access (read/write) data to DSS file
</li><li>depends on: hec module, *hecConfig.py
</li><li>GetMaxValueIndex(hydrograph): finds index of the maximum value in hydrograph</li></ul></p>

<h6>ExampleHydraulicComparison.py</h6>
<p><ul><li>description: retrieves hydraulic results from DSS file (does nothing with them yet)
</li><li>depends on: hec module, *hecConfig.py
</li><li>GetMaxValueIndex(hydrograph): finds index of the maximum value in hydrograph</li></ul></p>
