:: Script to run the ISWS InitHMS Python code that splits HEC-HMS subbasins
:: based on future redevelopment
::@ECHO OFF
SET PYTHON_DIR=c:\Python27
::SET PATH=%PYTHON_DIR%;%PATH%
SET pythonPath="%PYTHON_DIR%\python.exe"
CALL %pythonPath% HEC_Inundation.py > HEC_Inundation_out.txt
::CALL python HEC_Inundation.py > HEC_Inundation_out.txt