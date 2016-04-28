# Python class for all the functionality associated with
# the HEC "model" (which basically consists of accessing
# and modifying DSS files).
import ctypes, os
from subprocess import call
import pickle
import json

class Model:
    """Class that represents out HEC model"""
    def __init__(self):
        # obtain configuration details for HEC applications for
        # python and jython scripts
        import hecConfig
        reload(hecConfig)
        self.config = hecConfig.HecConfig()

    # TBD: Not sure if the script required for running HEC-HMS needs
    # to be different in steps 9 and 11. We currently assume HMS model
    # is in same location. If different, may need to run different
    # scritps within HEC-HMS
    def runHms(self):
        popd=os.getcwd()
        os.chdir(self.config.hmsDir)
        call([self.config.hmsCommand, "-s", self.config.scriptPath + "/RunHecHmsModel.py"], shell=True)
        os.chdir(popd)

    # Implements step 7 of the brief workflow description
    def newStorageOutflowCurves(self):
        popd=os.getcwd()
        os.chdir(self.config.dssDir)

        # write the sub basin release rates as a python pickle file as the json
        # module isn't available in the HEC-HMS Jython environment
        #        dtf = open(self.config.getDataTransferFilePath(),'w')
        tableFile = self.config.scriptPath + "/table_names.json"
        with open(tableFile, 'rb') as tF:
            tableNames = json.load(tF)
        dtf = open(self.config.getDataTransferFilePath(), 'w')
        import pickle
        pickle.dump(tableNames, dtf)
        dtf.close()

        call([self.config.dssCommand, "-s", self.config.scriptPath + "/dummyStorageOutflowCurves.py"], shell=True)
        os.chdir(popd)

    # Implements step 10 of the brief workflow description
    def createStorageOutflowCurves(self, subbasins):
        popd=os.getcwd();
        os.chdir(self.config.dssDir)

        # write the sub basin info as a python pickle file as the json
        # module isn't available in the HEC-HMS Jython environment
        dtf = open(self.config.getDataTransferFilePath(),'w')
        pickle.dump(subbasins,dtf)
        dtf.close()

        call([self.config.dssCommand, "-s", self.config.scriptPath + "/createStorageOutflowCurves.py"], shell=True)
        os.chdir(popd)

    # Implements step 10 of the brief workflow description
    def copyStorageOutflowCurves(self, subbasins):
        popd=os.getcwd();
        os.chdir(self.config.dssDir)

        # write the sub basin info as a python pickle file as the json
        # module isn't available in the HEC-HMS Jython environment
        dtf = open(self.config.getDataTransferFilePath(),'w')
        pickle.dump(subbasins,dtf)
        dtf.close()

        call([self.config.dssCommand, "-s", self.config.scriptPath + "/copyStorageOutflowCurves.py"], shell=True)
        os.chdir(popd)

    # Run the HWC-RAS model.
    def runRas(self):
        print "running HEC-RAS..."
        rasProjectFilePath = self.config.getRasProjectPath() + "/" + self.config.rasProjectName + ".prj"

        import time
        startTime = time.clock()
        import win32com.client
        rasController = win32com.client.Dispatch("RAS41.HECRASController")
        rasController.Project_Open(rasProjectFilePath)
        rasController.Compute_CurrentPlan()
        print("HEC-RAS completed in {0} seconds".format(time.clock() - startTime))

    # TODO: Eventually update this method to perform all the
    # comparison and generation functionality required by step
    # 16 of the example workflow. For now, just get some data from
    # the results of HEC-RAS and return this in JSON format
    def getHydraulicResults(self, ditchNames):
        popd=os.getcwd();
        os.chdir(self.config.dssDir)

        dtf = open(self.config.getDataTransferFilePath(),'w')
        pickle.dump(ditchNames,dtf)
        dtf.close()

        call([self.config.dssCommand, "-s", self.config.scriptPath + "/ExampleHydraulicComparison.py"], shell=True)
        dtf = open(self.config.getDataTransferFilePath(),'r+')
        data = dtf.read()
        dtf.close()
        os.remove(self.config.getDataTransferFilePath())
        os.chdir(popd)
        return data;
