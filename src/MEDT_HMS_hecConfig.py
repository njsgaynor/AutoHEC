# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HecConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        import parent_hecConfig
        self = parent_hecConfig.setme1(self)

        # HEC-HMS project configuration data
        self.hmsProjectPath = self.hmsVersion + "MelvinaDitch/MEDT_DesignRuns"
        self.osHmsProjectPath = self.osHmsVersion + "MelvinaDitch/MEDT_DesignRuns"
        # ["LucasDitch/LUDT_DesignRuns", "LucasDiversionDitch/LDDT_DesignRuns",
        #        "MelvinaDitch/MEDT_DesignRuns", "MPDT/MPDT_DesignRuns",
        #        "OakLawn/OLCR_DesignRuns", "StonyCreek/HMS/STCR_DesignRuns"]
        self.hmsProjectName = "MEDT_HMS"
        # ["LUDT_Design", "LDDT_HMS", "MEDT_HMS", "MPDT_revised", "OLCRHMS", "STCR_combined"]

        self = parent_hecConfig.setme2(self)
        self.basinin = self.hmsProjectPath + "/MEDT_Design - Copy.basin"
        self.basinout = self.hmsProjectPath + "/MEDT_Design.basin"

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getHmsProjectPath(self):
        return self.hmsProjectPath

    def getRasProjectPath(self):
        return self.rasProjectPath
