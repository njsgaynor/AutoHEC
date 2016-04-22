# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HMSConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        self.scriptPath="C:/Users/nschiff2/IdeaProjects/Optimatics_1.1/src" #
        self.HMSPath = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/Stony_V6.1optim/HydrologicModels/" \
                       "ExistingConditions/LucasDitch/LUDT_DesignRuns"
        self.basinin = self.scriptPath + "/HEC-HMSModels/LucasDitch/LUDT_DesignRuns/LUDT_Design - Copy.basin" #
        self.basinout = self.scriptPath + "/HEC-HMSModels/LucasDitch/LUDT_DesignRuns/LUDT_Design.basin" #
        self.pdatafile = self.scriptPath + "/HEC-HMSModels/LucasDitch/LUDT_DesignRuns/LUDT_Design.pdata" #
        self.dssfile = self.scriptPath + "/HEC-HMSModels/LucasDitch/LUDT_DesignRuns/LUDT_Design.dss" #
        self.stationFileName = self.scriptPath + "/HEC-HMSModels/LucasDitch/LUDT_DesignRuns/StationList_StonyCreek.txt" #
        self.inputFileName = self.scriptPath + "/HEC-HMSModels/LucasDitch/LUDT_DesignRuns/LUDT_input.json" #
        self.redevelopment = 15 #
        self.curvenumber = 88 #
        self.releaserate = 0.15 #

        # HEC-HMS project configuration data
 #       self.hmsProjectName="LUDT_Design"
 #       self.hmsRunName="100yr12hrHuffARF"
        self.hmsMetFile = "HuffQII_100yr12hr" #
        self.hmsGageName = "100YR12HRHUFFARF" #

    def getHmsProjectPath(self):
        return self.scriptPath + "/HEC-HMSModels/LucasDitch/LUDT_DesignRuns" #