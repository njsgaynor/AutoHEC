class CompareConfig:
    """

    """
    def __init__(self):
        ## USC options
        self.filePath = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/USC/"
        self.versionPath = self.filePath + "USC_V"
        self.dssRasFileName = "/Base_and_Calibration.dss"
        self.dssHmsFilePath = "/"
        self.dssHmsFileName = [self.dssHmsFilePath + "USC.dss"]
        self.rasRunName = "ILREVEXIMP040512"
        #self.hmsRunName = "100-24"
        self.startDate = "01DEC2007"

        ## STCR options
        # self.filePath = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/"
        # self.versionPath = self.filePath + "Stony_V"
        # self.dssRasFileName = "/HydraulicModels/ExistingConditions/STCR/STCR_DesignRuns/STCR_Design2.dss"
        # self.dssHmsFilePath = "/HydrologicModels/ExistingConditions/"
        # self.dssHmsFileName = [self.dssHmsFilePath + "LucasDitch/LUDT_DesignRuns/LUDT_Design.dss",
        #             self.dssHmsFilePath + "LucasDiversionDitch/LDDT_DesignRuns/LDDT_HMS.dss",
        #             self.dssHmsFilePath + "MelvinaDitch/MEDT_DesignRuns/MEDT_HMS.dss",
        #             self.dssHmsFilePath + "MPDT/MPDT_DesignRuns/MPDT_revised.dss",
        #             self.dssHmsFilePath + "OakLawn/OLCR_DesignRuns/OLCRHMS.dss",
        #             self.dssHmsFilePath + "StonyCreek/HMS/STCR_DesignRuns/STCR_combined.dss"]
        # self.runName = "HUFFQII_100YR12H" #"100YR24HRISWS" #
        # self.startDate = "01DEC2006"

        ## Global options
        self.dataPath = ""  #not currently used
        # baseVersions and compareVersions must be the same length
        self.baseVersions = ["9.0optim"] #"8.0","9.0","11.0"]
        self.compareVersions = ["9.0optim"] #"8.0optim","9.0optim","11.0optim"]