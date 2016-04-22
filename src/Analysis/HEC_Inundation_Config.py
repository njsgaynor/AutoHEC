class BankStation_config:
    """
    --bankFileName needs to be created manually from HEC-RAS output of LOB elev and ROB elev.
    Fields are river, reach, station ID, LOB elev, and ROB elev.
    --filePath is the path to the HEC-RAS DSS file
    --dssFileName is the exact DSS file that contains the data you want to analyze
    --outFileName is the CSV file that will contain the out-of-banks data
    --runName is a specific run within the DSS file
    --startDate is the beginning date of the RAS run, format: ddMMMyyyy
    """
    def __init__(self):
        ## When preparing the bank station elevations file, do not include Node Names in the table (under
        ## Options menu in the Profile Output Table of HEC-RAS).
        self.version = "2.0"
        self.bankFileName = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/StonyCreek_banks2.csv" # "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/USC/USC_banks2.csv"
        self.filePath = "G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/StonyCreek/Stony_V" + self.version + "/" #"G:/PROJECTS_non-FEMA/MWRD_ReleaseRate_Phase1/H&H/USC/USC_V4.0/"
        self.dataPath = self.filePath + "HydraulicModels/ExistingConditions/STCR/STCR_DesignRuns/"
        self.dssFileName = self.dataPath + "STCR_Design2.dss" #"Base_and_Calibration.dss"
        self.outFileName = self.filePath + "OOB_StonyCreek_V" + self.version + ".csv" #"OOB_USC.csv"
        self.runName = "100YR24HRISWS" #"HUFFQII_100YR12H" #"ILREVEXIMP040512" #
        self.startDate = "01DEC2006" #"01DEC2007" #
