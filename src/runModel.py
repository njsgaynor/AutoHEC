#!/usr/bin/python
# Script to execute the ISWS HEC-HMS and HEC-RAS model

import json, os, sys, shutil
import SplitBasins.InitHMS

# read JSON data from stdin
subsubwatersheds = sys.stdin.readlines()
for item in range(len(subsubwatersheds)):
    subsubwatersheds[item] = subsubwatersheds[item].strip('\r\n')

for s in subsubwatersheds:
    print(s + str(len(subsubwatersheds)) + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # rename config file for use in scripts
    backupFileName = s + "_hecConfig.py"
    #os.rename(backupFileName, "hecConfig.py")

    # obtain configuration details for HEC applications for
    # python and jython scripts
    try:
        os.remove("hecConfig.pyc")
        os.remove("hecConfig$py.class")
    except Exception, e:
        print("hecConfig.pyc or hecConfig$py.class does not yet exist.")
    shutil.copyfile(backupFileName, "hecConfig.py")
    import hecConfig
    reload(hecConfig)
    config = hecConfig.HecConfig()
    try:
        os.remove(config.modelVersion + "parent_hecConfig.py")
        os.remove(config.modelVersion + "parent_hecConfig_USC.py")
    except Exception, e:
        print("parent_hecConfig.py or parent_hecConfig_USC.py has never been copied for this model version.")
    shutil.copyfile("parent_hecConfig.py", config.modelVersion + "parent_hecConfig.py")
    shutil.copyfile("parent_hecConfig_USC.py", config.modelVersion + "parent_hecConfig_USC.py")
    curdir = os.getcwd()
    os.chdir(config.scriptPath)
    #print(vars(config))

    # STEPS 03-06: split subbasins and assign future properties
    print("Creating redeveloped subbasins...")
    SplitBasins.InitHMS.main(config)

    swStructure = json.load(open(config.inputFileName, 'rb'))
    subbasins = swStructure['subbasins']
    ditchNames = swStructure['ditchNames']
    print("Input file name: " + config.inputFileName)
    print(subbasins)

    # obtain instance of our HEC "model"
    from hecModel import Model
    model = Model()

    # STEPS 07-08: create dummy storage-outflow curves
    print("new curves")
    model.newStorageOutflowCurves()

    # STEP 09: run HEC-HMS model
    print("Running HEC-HMS the first time...")
    model.runHms()

    # Step 10: build storage curves
    # Create for a 24h storm or copy for a 12h storm
    # The 24h storm must run before the 12h storm
    if "12" in config.hmsRunName:
        print("Copying storage-outflow curves...")
        model.copyStorageOutflowCurves(subbasins)
    elif "24" in config.hmsRunName:
        print("Creating storage-outflow curves...")
        model.createStorageOutflowCurves(subbasins)
    else:
        print("Can't tell if 12h or 24h precipitation.")

    # Step 11: run HEC-HMS model
    print("Running HEC-HMS the second time...")
    model.runHms()

    # move config file back to original file name
    #os.rename("hecConfig.py", backupFileName)

# Step 12
# No automation required for this step.

# Step 13
# Model runtimes are currently short enough to ignore this step

# Step 14
# TBD - Need to clarify if this step is necessary

# Step 15: run HEC-RAS model
os.chdir(curdir)
model.runRas()
os.chdir(config.scriptPath)

# Step 16
# Compare, process and return the hydraulic results on the standard
# output in JSON format
#hydraulicResults = model.getHydraulicResults(ditchNames)
#sys.stdout.write(json.dumps(hydraulicResults))
