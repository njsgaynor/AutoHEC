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
        self.hmsRunName = "100-24"
        self.startDate = "01DEC2007"
        self.watershed = "USC"
        self.timestep = 6.0

        ## STCR options
        # self.scriptPath = "C:/Users/nschiff2/IdeaProjects/AutoHEC/src/Analysis/"
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
        # self.bankFileName = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/StonyCreek_banks2.csv" #CSV file
        # self.inundOutFileName = self.filePath + "OOB_StonyCreek_V"
        # self.rasRunName = "HUFFQII_100YR12H" #"100YR24HRISWS" #
        # self.startDate = "01DEC2006"
        # self.watershed = "StonyCreek"
        # self.timestep = 5.0

        ## Global options
        # Model versions to analyze
        # --first item is considered the base model
        # --max of 5 for now
        # --cannot use a non-redeveloped model as the first model when plotting rating curves
        self.versions = ["15.0optim"]#["2.0", "17.0optim", "23.0optim"] #,"16.0optim", "22.0optim"
                        #["2.0","3.0optim","4.0optim","5.0optim","6.0optim","7.0","8.0","9.0optim",
                        # "10.0optim","11.0optim","11.1optim","12.0optim","12.1optim","13.0optim",
                        # "14.0optim","15.0optim","16.0optim","17.0optim","19.0optim","21.0optim",
                        # "22.0optim","23.0optim","24.0optim"]
        # Description of each plotted/analyzed model version, used for figure legends
        self.vDescription = ["40% Development; 0.3 cfs/acre, CN 73 (v15)"] #["DWP Base Model (v2)",
                             # "40% Development; WB/MS34-MS40/MS42 0.25, AH01-AH12 0.2, rest 0.3 cfs/acre (v17)",
                             # "40% Development; WB/MS34-MS40/MS42 0.2, AH01-AH12 0.15, rest 0.3 cfs/acre (v23)"]
                             # "15% Development; WB/MS34-MS40/MS42 0.25, AH01-AH12 0.2, rest 0.3 cfs/acre (v16)",
                             # "15% Development; WB/MS34-MS40/MS42 0.2, AH01-AH12 0.15, rest 0.3 cfs/acre (v22)"]