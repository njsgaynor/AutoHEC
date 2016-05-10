# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HecConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        import parent_hecConfig
        self = parent_hecConfig.setme1(self)

        # HEC-HMS project configuration data
        self.hmsProjectPath = self.hmsVersion + "MPDT/MPDT_DesignRuns"
        self.osHmsProjectPath = self.osHmsVersion + "MPDT/MPDT_DesignRuns"
        # ["LucasDitch/LUDT_DesignRuns", "LucasDiversionDitch/LDDT_DesignRuns",
        #        "MelvinaDitch/MEDT_DesignRuns", "MPDT/MPDT_DesignRuns",
        #        "OakLawn/OLCR_DesignRuns", "StonyCreek/HMS/STCR_DesignRuns"]
        self.hmsProjectName = "MPDT_revised"
        # ["LUDT_Design", "LDDT_HMS", "MEDT_HMS", "MPDT_revised", "OLCRHMS", "STCR_combined"]

        self = parent_hecConfig.setme2(self)
        self.hmsMetFile = self.hmsProjectPath + "/100yr12hrHuff"
        self.hmsGageName = "100yr12hrHuff"
        self.basinin = self.hmsProjectPath + "/MPDT_levelpool - Copy.basin"
        self.basinout = self.hmsProjectPath + "/MPDT_levelpool.basin"

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getHmsProjectPath(self):
        return self.hmsProjectPath

    def getRasProjectPath(self):
        return self.rasProjectPath
