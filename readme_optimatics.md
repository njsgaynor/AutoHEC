HEC-RAS Integration
===================

Background
----------

Developed for use by Illinois State Water Survey.

Phase 1 zip package sent to Josh 2015-02-15 can be found at: https://s3.amazonaws.com/optimatics/temp/optimizer-hecras-integration.zip

Technical
---------

- The GIT repository is located [here](https://bitbucket.org/optimatics/optimizer-hecras-integration).
- JIRA has Epics for [Phase One](https://optimatics.atlassian.net/browse/OM-4032) and [Phase Two](https://optimatics.atlassian.net/browse/OM-40730.
- Detailed technical documentation on [Confluence](https://optimatics.atlassian.net/wiki/display/DEV/HEC+Suite).

Prerequisites
-------------

- Python 2.7.11 (install "just for me" to "C:\Python27").
- Python for Windows [Extensions](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win32-py2.7.exe/download) x86 v219 (required for COM manipulation).
- HEC-RAS 4.1.0 must be installed on the system for correct registration of COM objects.

Execution
---------

- On line 7 of "hecConfig.py", set "scriptPath" to the full path of the "src" directory.
- In the "src" directory execute "runModel.cmd".
