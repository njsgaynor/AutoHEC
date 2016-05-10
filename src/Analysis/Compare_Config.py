class CompareConfig:
    """

    """
    def __init__(self):
        ## USC options
        self.scriptPath = "C:/Users/nschiff2/IdeaProjects/AutoHEC/src/Analysis/"
        self.filePath = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/USC/"
        self.versionPath = self.filePath + "USC_V"
        self.dssRasFileName = "/Base_and_Calibration.dss"
        self.dssHmsFilePath = "/"
        self.dssHmsFileName = [self.dssHmsFilePath + "USC.dss"]
        self.bankFileName = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/USC/USC_banks2.csv" #CSV file
        self.inundOutFileName = self.filePath + "OOB_USC_V"
        self.rasRunName = "ILREVEXIMP040512"
        #self.hmsRunName = "100-24"
        self.startDate = "01DEC2007"
        self.watershed = "USC"

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
        # self.rasRunName = "100YR24HRISWS" #"HUFFQII_100YR12H" #
        # self.startDate = "01DEC2006"
        # self.watershed = "StonyCreek"

        ## Global options
        # Model versions to analyze
        # --first item is considered the base model
        # --max of 5 for now
        # --cannot use a non-redeveloped model as the first model when plotting rating curves
        self.versions = ["2.0", "6.0optim", "6.1optim"]