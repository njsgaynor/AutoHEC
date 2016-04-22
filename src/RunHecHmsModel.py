# Jython script to run a HEC-HMS model

# obtain configuration details for HEC applications for
# python and jython scripts
import hecConfig
reload(hecConfig)
config = hecConfig.HecConfig()

# perform run
from hms.model.JythonHms import OpenProject,Compute,Exit
OpenProject(config.hmsProjectName,config.getHmsProjectPath())
Compute(config.hmsRunName)
Exit(1)
