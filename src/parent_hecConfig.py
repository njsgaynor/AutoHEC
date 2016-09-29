# Configuration that is used through all HEC Python/Jython scripts
# **You need to comment out some lines in the MPDT and StonyCreek
#   configuration files when running the 24hr version.**

def setme1(self):
    # General model settings
    # *only the below options should be changed*
    # --scriptPath is the location of the scripts in the AutoHEC package;
    #   it should end with "AutoHEC/src"
    # --modelPath is the location of the model run files
    # --modelVersion is the directory name of the model version
    self.scriptPath="C:/Users/nschiff2/IdeaProjects/AutoHEC/src"
    self.hmsDir="HEC-HMS"
    self.modelPath = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/"
    self.modelVersion = self.modelPath + "Stony_test/"
    self.hmsVersion = self.modelVersion + "HydrologicModels/ExistingConditions/"
    self.hmsCommand="HEC-HMS.cmd"
    self.dssDir="HEC-DSSVue"
    self.dssCommand="HEC-DSSVue.cmd"

    # Use these options only when you need a different model version to build the
    # storage-outflow curves
    self.osModelVersion = self.modelPath + "Stony_test_24/"
    self.osHmsVersion = self.osModelVersion + "HydrologicModels/ExistingConditions/"

    return self

def setme2(self):
    # HMS precipitation settings
    # --hmsRunName is the name of the compute option you would choose in HEC-HMS
    # --hmsMetFile is the location of the relevant *.met file for hmsRunName
    # --hmsGageName is the name of the gage shown in the hmsMetFile
    self.hmsRunName = "100YR12HRHUFFARF" #"HuffQII_100yr12hrISWS" #"HuffQIII_100yr24hrISWS" #
    self.hmsMetFile = self.hmsProjectPath + "/HuffQII_100yr12hr" #"/HuffQII_100yr12hrISWS" #"/HuffQIII_100yr24hrISWS" #
    self.hmsGageName = "100YR12HRHUFFARF" #"HuffQII_100yr12hrISWS" #"HuffQIII_100yr24hrISWS" #
    # self.hmsRunName = "HuffQIII_100yr24hrISWS"
    # self.hmsMetFile = self.hmsProjectPath + "/HuffQIII_100yr24hrISWS"
    # self.hmsGageName = "HuffQIII_100yr24hrISWS"

    # Future parameters
    # --redevelopment is the proportion of the subbasin that is routed
    #   through the new reservoir
    # --curvenumber is the curve number for all subbasins
    # --releaserate is the release rate for all subbasins; this can
    #   be adjusted by subbasin if you run InitHMS.py separate from
    #   the model runs, manually edit subbasin_records.json, and then
    #   run HEC-HMS and HEC-RAS.
    # --releaseratealt is the alternative release rate for the subbasins
    #   listed in alt_RR_basins.txt in the version home directory
    self.redevelopment = 15
    self.redevelopmentalt = 15
    self.redevelopmentalt2 = 15
    self.curvenumber = 88
    self.releaserate = 0.3
    self.releaseratealt = 0.3
    self.releaseratealt2 = 0.3
    self.canopyrate = 0.52
    self.canopyalt = 0.26

    # HMS project configuration data
    # --numHmsModels is the number of HMS model runs needed for a single RAS run
    # --interval is the output time interval of FLOW in the RAS DSS file
    # --intervalNum is a plain integer version of interval
    # --basinin, basinout, pdatafile, dssfile, osDssFile, and inputFileName
    #   specify file names for files used in the model run. osDssFile is used
    #   only if you want to use a different DSS file to build the storage-outflow
    #   curves. inputFileName is automatically generated and should not be changed.
    self.numHmsModels = 6
    self.interval = "5MIN"
    self.intervalNum = 5
    self.basinin = self.hmsProjectPath + "/" + self.hmsProjectName + " - Copy.basin"
    self.basinout = self.hmsProjectPath + "/" + self.hmsProjectName + ".basin"
    self.pdatafile = self.hmsProjectPath + "/" + self.hmsProjectName + ".pdata"
    self.dssfile = self.hmsProjectPath + "/" + self.hmsProjectName + ".dss"
    self.osDssFile = self.osHmsProjectPath + "/" + self.hmsProjectName + ".dss"
    # Do not change inputFileName
    self.inputFileName = self.hmsProjectPath + "/" + self.hmsProjectName + "_input.json"

    # HEC-RAS project configuration data
    # --rasProjectName is the name of the RAS *.dss file
    # --rasPlanName is the plan name that shows up in DSSVue when you look
    #   at the DSS file
    # --rasProjectPath is the location of the RAS project files
    # --stationFileName is the location of a text file that lists all the
    #   station names, one per line (usually the home directory of a watershed)
    self.rasProjectName = "STCR_Design"
    self.rasPlanName = "100YR12HRHuffQII" #"HUFFQIII_100YR24HRISWS" #
    self.rasProjectPath = self.modelVersion + "HydraulicModels/ExistingConditions/STCR/STCR_DesignRuns"
    self.stationFileName = self.modelPath + self.rasProjectName + "_StationList.txt"

    return self
