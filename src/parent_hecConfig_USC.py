# Configuration that is used through all HEC Python/Jython scripts
# see documentation in hecConfig.md

def setme1(self):
    self.scriptPath="C:/Users/nschiff2/IdeaProjects/AutoHEC/src"
    self.hmsDir="HEC-HMS"
    self.modelPath = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/USC/"
    self.modelVersion = self.modelPath + "USC_V10.0optim"
    self.hmsVersion = self.modelVersion
    self.hmsCommand="HEC-HMS.cmd"
    self.dssDir="HEC-DSSVue"
    self.dssCommand="HEC-DSSVue.cmd"

    self.osModelVersion = self.modelPath + "USC_V10.0optim"
    self.osHmsVersion = self.osModelVersion
    #self.rasDir="HEC-RAS"
    #self.rasDll="ras.exe"

    return self

def setme2(self):
    self.hmsRunName = "100-24" #"HuffQII_100yr12hrISWS" #"HuffQIII_100yr24hrISWS"
    self.hmsMetFile = self.hmsProjectPath + "/100_24" #"/HuffQII_100yr12hrISWS" #"/HuffQIII_100yr24hrISWS"
    self.hmsGageName = "100-24" #"HuffQII_100yr12hrISWS" #"HuffQIII_100yr24hrISWS"

    self.redevelopment = 15
    self.curvenumber = 88
    self.releaserate = 0.25

    self.numHmsModels = 1
    self.interval = "6MIN"
    self.intervalNum = 6
    self.basinin = self.hmsProjectPath + "/Clark_1_new_Tc.basin.backup"
    self.basinout = self.hmsProjectPath + "/Clark_1_new_Tc.basin"
    self.pdatafile = self.hmsProjectPath + "/" + self.hmsProjectName + ".pdata"
    self.dssfile = self.hmsProjectPath + "/" + self.hmsProjectName + ".dss"
    self.osDssFile = self.osHmsProjectPath + "/" + self.hmsProjectName + ".dss"
    self.inputFileName = self.hmsProjectPath + "/" + self.hmsProjectName + "_input.json"

    # HEC-RAS project configuration data
    self.rasProjectName="Base_and_Calibration"
    self.rasPlanName = "ISWSRevisedProposed_04052012"
    self.rasProjectPath = self.modelVersion
    self.stationFileName = self.modelPath + self.rasProjectName + "_StationList.txt"

    return self

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getHmsProjectPath(self):
        return self.hmsProjectPath

    def getRasProjectPath(self):
        return self.rasProjectPath