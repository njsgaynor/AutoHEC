#!/usr/bin/python

# Jython 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Last updated: March 2016

# add directories to system path
import sys
import os
import shutil

sys.path.append("C:/Program Files/Java/jdk1.8.0_72/bin/java.exe")
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/src/java")
sys.path.append("C:/Program Files/Java/javahelp-2.0.05.jar")
sys.path.append("../.")

from Subwatershed_class import Subwatershed

def copyFiles(ws, metFile):
    # Create backup/source copy of *.basin file
    if os.path.isfile(ws['basinin']):
        os.remove(ws['basinout'])
        os.rename(ws['basinin'], ws['basinout'])
        shutil.copyfile(ws['basinout'], ws['basinin'])
    else:
        shutil.copyfile(ws['basinout'], ws['basinin'])
    # Create backup copy of *.pdata file
    if os.path.isfile(ws['pdatafile'] + ".backup"):
        os.remove(ws['pdatafile'])
        os.rename(ws['pdatafile'] + ".backup", ws['pdatafile'])
        shutil.copyfile(ws['pdatafile'], ws['pdatafile'] + ".backup")
    else:
        shutil.copyfile(ws['pdatafile'], ws['pdatafile'] + ".backup")
    # Create backup copy of HMS *.dss file
    if os.path.isfile(ws['dssfile'] + ".backup"):
        os.remove(ws['dssfile'])
        os.rename(ws['dssfile'] + ".backup", ws['dssfile'])
        shutil.copyfile(ws['dssfile'], ws['dssfile'] + ".backup")
    else:
        shutil.copyfile(ws['dssfile'], ws['dssfile'] + ".backup")
    # Create backup copy of *.met file
    if os.path.isfile(metFile + ".backup"):
        os.remove(metFile)
        os.rename(metFile + ".backup", metFile)
        shutil.copyfile(metFile, metFile + ".backup")
    else:
        shutil.copyfile(metFile, metFile + ".backup")


def readBasinFile(ws, scriptPath, modelVersion):
    from hecElements.Basin_class import Basin
    from hecElements.Subbasin_class import Subbasin
    from hecElements.Junction_class import Junction
    from hecElements.Reservoir_class import Reservoir
    from hecElements.Reach_class import Reach
    from hecElements.Diversion_class import Diversion
    from hecElements.Sink_class import Sink
    from hecElements.BasinSchema_class import BasinSchema
    from TableNames_class import TableNames
    from hecElements.Pdata_class import Pdata
    from SBList_class import SBList

    pdatabackup = ws['pdatafile'] + ".back"
    tableFile = scriptPath + "/table_names.json"
    print(tableFile)
    subbasinFile = scriptPath + "/subbasin_records.json"
    print(subbasinFile)
    # Make backup of *.pdata file
    shutil.copyfile(ws['pdatafile'], pdatabackup)
    altRRfile = open(modelVersion + "alt_RR_basins.txt", 'rb')
    altRRlist = altRRfile.readlines()
    altRRfile.close()
    altRRlist[:] = [r.strip('\n').strip('\r').upper() for r in altRRlist]
    print altRRlist
    # Read elements from *.basin file and split the subbasins; write to new *.basin file
    # Also create list of table names (txt) and and subbasins/release rates (JSON) and write to files for later use
    with open(ws['basinin'], 'rb') as basinsrc, open(ws['basinout'], 'wb') as basinsink, open(ws['pdatafile'], 'ab') \
            as pdatasink:
        tableList = TableNames()
        sbAll = SBList()
        recordnum = 0
        currentLine = ' '
        while not currentLine == '':
            try:
                currentLine = basinsrc.readline()
                if(currentLine.startswith('End:')):
                    try:
                        b.serialize(basinsink)
                        recordnum += 1
                    except:
                        print("Unexpected 'End:' statement in " + ws['basinin'] + ". Exiting.")
                        return
                elif currentLine.startswith('Basin:'):
                    b = Basin.readBasin(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Subbasin:'):
                    b, b2, soname = Subbasin.readSubbasin(currentLine, basinsrc, basinsink, ws['redevelopment'],
                                                      ws['curvenumber'], ws['releaserate'], altRRlist, ws['releaseratealt'])
                    if b.getIdentifier() in altRRlist:
                        tableList.append([b2.getIdentifier(), soname, b2.area.getAsFloat(), ws['releaseratealt']])
                        sbAll.newItem(b.getIdentifier(), float(ws['releaseratealt']), b.area.getAsFloat(), '')
                        sbAll.newItem(b2.getIdentifier(), float(ws['releaseratealt']), b2.area.getAsFloat(), soname)
                    else:
                        tableList.append([b2.getIdentifier(), soname, b2.area.getAsFloat(), ws['releaserate']])
                        sbAll.newItem(b.getIdentifier(), float(ws['releaserate']), b.area.getAsFloat(), '')
                        sbAll.newItem(b2.getIdentifier(), float(ws['releaserate']), b2.area.getAsFloat(), soname)
                    Pdata.newPdata(soname, pdatasink, ws['dssfile'])
                elif currentLine.startswith('Junction:'):
                    b = Junction.readJunction(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Reservoir:'):
                    b = Reservoir.readReservoir(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Reach:'):
                    b = Reach.readReach(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Diversion:'):
                    b = Diversion.readDiversion(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Sink:'):
                    b = Sink.readSink(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Basin Schematic Properties:'):
                    b = BasinSchema.readBasinSchema(currentLine, basinsrc, basinsink)
                elif currentLine.endswith('\n'):
                    pass
                elif currentLine == '':
                    print("End of file " + ws['basinin'] + ".")
                    try:
                        tableList.writeTableFile(tableFile)
                    except IOError:
                        print("Cannot write table_names.json")
                    try:
                        sbAll.writeSbPairs(subbasinFile)
                        print(subbasinFile)
                    except IOError:
                        print("Cannot write subbasin_records.json")
                    return tableList, sbAll
                else:
                    print(currentLine)
                    raise RuntimeError("Invalid subwatershed element. Check input *.basin file.")
            except IOError:
                print("Cannot read file " + ws['basinin'] + " or " + ws['basinout'] + ".")
                return


def readList(fileName):
    with open(fileName, 'rb') as fileObj:
        listObj = fileObj.readlines()
    for item in range(len(listObj)):
        listObj[item] = listObj[item].strip('\r\n')
    return listObj


def writeJsonInput(subbasinList, stationList, inputFileName):
    import json
    outputDS = {"subbasins": subbasinList, "ditchNames": stationList}
    with open(inputFileName, 'wb') as inputFile:
        json.dump(outputDS, inputFile)


def modMetFile(metFile, metData, sbList):
    metFileName = metFile
    print(metFile)
    with open(metFileName, 'ab') as metFileObj:
        metFileObj.write('\n\n')
        for subbasin in sbList:
            lines = ['Subbasin: ', subbasin[0], '\n     Gage: ', metData, '\n\n     Begin Snow: None\nEnd:\n\n']
            metFileObj.writelines(lines)


def main(config):
    metFile = config.hmsMetFile + ".met"
    ws = Subwatershed(config)
    copyFiles(ws, metFile)
    tableList, subbasinList = readBasinFile(ws, config.scriptPath, config.modelVersion)
    stationList = readList(config.stationFileName)
    writeJsonInput(subbasinList, stationList, config.inputFileName)
    modMetFile(metFile, config.hmsGageName, tableList)


if __name__=="__main__":
    from src import hecConfig
    reload(hecConfig)
    config = hecConfig.HecConfig()
    main(config)
