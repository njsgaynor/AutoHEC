# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

#class ParentHecConfig:
#    """Simple class maintaining configuration for HEC applications"""
#    def __init__(self):

def setme1(self):
    self.scriptPath="C:/Users/nschiff2/IdeaProjects/AutoHEC/src"
    self.hmsDir="HEC-HMS"
    self.modelPath = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/"
    self.modelVersion = self.modelPath + "Stony_V4.0optim/"
    self.hmsVersion = self.modelVersion + "HydrologicModels/ExistingConditions/"
    self.hmsCommand="HEC-HMS.cmd"
    self.dssDir="HEC-DSSVue"
    self.dssCommand="HEC-DSSVue.cmd"

    self.osModelVersion = self.modelPath + "Stony_V5.0optim/"
    self.osHmsVersion = self.osModelVersion + "HydrologicModels/ExistingConditions/"
    #self.rasDir="HEC-RAS"
    #self.rasDll="ras.exe"

    return self

def setme2(self):
    self.hmsRunName = "100YR12HRHUFFARF" #"HuffQII_100yr12hrISWS" #"HuffQIII_100yr24hrISWS"
    self.hmsMetFile = self.hmsProjectPath + "/HuffQII_100yr12hr" #"/HuffQII_100yr12hrISWS" #"/HuffQIII_100yr24hrISWS"
    self.hmsGageName = "100YR12HRHUFFARF" #"HuffQII_100yr12hrISWS" #"HuffQIII_100yr24hrISWS"
    #self.hmsRunName = "HuffQIII_100yr24hrISWS"
    #self.hmsMetFile = self.hmsProjectPath + "/HuffQIII_100yr24hrISWS"
    #self.hmsGageName = "HuffQIII_100yr24hrISWS"

    self.redevelopment = 15
    self.curvenumber = 88
    self.releaserate = 0.15

    self.numHmsModels = 6
    self.interval = "5MIN"
    self.basinin = self.hmsProjectPath + "/" + self.hmsProjectName + " - Copy.basin"
    self.basinout = self.hmsProjectPath + "/" + self.hmsProjectName + ".basin"
    self.pdatafile = self.hmsProjectPath + "/" + self.hmsProjectName + ".pdata"
    self.dssfile = self.hmsProjectPath + "/" + self.hmsProjectName + ".dss"
    self.osDssFile = self.osHmsProjectPath + "/" + self.hmsProjectName + ".dss"
    self.inputFileName = self.hmsProjectPath + "/" + self.hmsProjectName + "_input.json"

    # HEC-RAS project configuration data
    self.rasProjectName = "STCR_Design"
    self.rasPlanName = "100YR12HRHuffQII" #"HUFFQIII_100YR24HRISWS"
    self.rasProjectPath = self.modelVersion + "HydraulicModels/ExistingConditions/STCR/STCR_DesignRuns"
    self.stationFileName = self.modelPath + "/" + self.rasProjectName + "_StationList.txt"

    return self
