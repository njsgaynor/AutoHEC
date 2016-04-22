# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HecConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        import parent_hecConfig
        self = parent_hecConfig.setme1(self)

        # HEC-HMS project configuration data
        self.hmsProjectPath = self.hmsVersion + "LucasDiversionDitch/LDDT_DesignRuns"
        self.osHmsProjectPath = self.osHmsVersion + "LucasDiversionDitch/LDDT_DesignRuns"
        # ["LucasDitch/LUDT_DesignRuns", "LucasDiversionDitch/LDDT_DesignRuns",
        #        "MelvinaDitch/MEDT_DesignRuns", "MPDT/MPDT_DesignRuns",
        #        "OakLawn/OLCR_DesignRuns", "StonyCreek/HMS/STCR_DesignRuns"]
        self.hmsProjectName = "LDDT_HMS"
        # ["LUDT_Design", "LDDT_HMS", "MEDT_HMS", "MPDT_revised", "OLCRHMS", "STCR_combined"]

        self = parent_hecConfig.setme2(self)
        self.basinin = self.hmsProjectPath + "/LDDT_Design - Copy.basin"
        self.basinout = self.hmsProjectPath + "/LDDT_Design.basin"

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getHmsProjectPath(self):
        return self.hmsProjectPath

    def getRasProjectPath(self):
        return self.rasProjectPath
