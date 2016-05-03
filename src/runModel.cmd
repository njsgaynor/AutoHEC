:: Script to run the ISWS HEC-HMS and HEC-RAS models with example sub basin release rates 
@ECHO OFF
SET PYTHON_DIR=c:\Python27
::SET PATH=%PYTHON_DIR%;%PATH%
SET pythonPath="%PYTHON_DIR%\python.exe"
::CALL %pythonPath% runModel.py < STCR.txt > output.txt
CALL %pythonPath% runModel.py < USC.txt > output.txt

