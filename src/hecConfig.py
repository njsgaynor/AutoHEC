# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HecConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        import parent_hecConfig_USC
        self = parent_hecConfig_USC.setme1(self)

        # HEC-HMS project configuration data
        self.hmsProjectPath = self.hmsVersion
        self.osHmsProjectPath = self.osHmsVersion
        self.hmsProjectName = "USC"

        self = parent_hecConfig_USC.setme2(self)

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getHmsProjectPath(self):
        return self.hmsProjectPath

    def getRasProjectPath(self):
        return self.rasProjectPath
