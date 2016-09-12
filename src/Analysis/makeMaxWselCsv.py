# Python 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date last updated: March 2016

# This program takes FLOW data from the HEC-RAS model and compares the hydrographs of different
# versions of the same river/reach. What is the output format?

import csv
import math
from Compare_Config import CompareConfig
from subprocess import call
import pickle
import os

def getData():
    """Get data from a DSS file"""
    popd=os.getcwd()
    dssvuePath = "C:/Program Files (x86)/HEC/HEC-DSSVue/"
    os.chdir(dssvuePath)
    # Path to script that extracts data from DSS file
    scriptPath = "C:/Users/nschiff2/IdeaProjects/AutoHEC/src/Analysis/"
    # Use HEC-DSSVue to run script (only way to use hec package that accesses DSS files)
    call(["HEC-DSSVue.cmd", "-s", scriptPath + "getPeakData.py"], shell=True)
    os.chdir(popd)

def roundSigfigs(num, sigfigs):
    """Round to specified number of sigfigs.
    from http://code.activestate.com/recipes/578114-round-number-to-specified-number-of-significant-di/
    accessed 3/24/2016"""
    if num != 0:
        return str(round(num, -int(math.floor(math.log10(abs(num))) - (sigfigs - 1))))
    else:
        return str(0.0)  # Can't take the log of 0


def readFromFile(filePath, fileName):
    # Loads flow data from specified versions, stored as dict
    return pickle.load(open(filePath + fileName, 'rb'))


def reassignKeys(dataDict):
    keyList = dataDict.keys()
    newDataDict = {}
    # Get rid of interpolated stations
    for key in keyList:
        # Extract station ID from data address in DSS file
        u = key.split('/')
        # Station ID needs to be greater than zero and numeric
        # * indicates interpolated station, letters indicate possible structure, 0.0 is origin station
        try:
            if(float(u[2]))>0:
                u[2] = roundSigfigs(float(u[2]), 7)  # eight characters/seven sig figs allowed
                newKey = " ".join(u[1:3])  # river/reach
                newDataDict[newKey] = dataDict.pop(key)# + dataAddress + runName + "/")
            else:
                print("Popping " + key)
                dataDict.pop(key)# + dataAddress + runName + "/")
        except ValueError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
            print("ValueError:", key)
    return newDataDict


def filterStations(filePath):
    # Reformat the station IDs listed in the CSV file. Later use this list to filter which stations are included.
    # The list is from the GIS people who are making the maps since not all cross sections are on the maps.
    with open(filePath + "USC_MEEKMA_XS.csv", 'rb') as inputFile: #"StonyCkXS_Zoe.csv", 'rb') as inputFile:  #
        stationList = []
        stationAddress = {}
        reader = csv.reader(inputFile)
        for row in reader:
            r = row
            if 'STONY' in r[0].upper():
                rdiv = [r[0],r[1],str(float(r[2])/5280.0)]
            else:
                rdiv = r
            try:
                rdiv[2] = roundSigfigs(float(rdiv[2]), 8)
            except Exception, e:
                print(e)
            stationList.append(' '.join(rdiv).upper())
            stationAddress[' '.join(rdiv).upper()] = '/'.join(r).upper()
    return stationList, stationAddress


def splitKey(k):
    # Split the key to get river, reach, and station ID as separate variables
    sKey = k.split('/')
    return [sKey[0], sKey[1], sKey[2]]


def removePeriod(versions):
    # The GIS software doesn't like periods in column headers, so replace them with underscores
    versions2 = versions[:]
    for v in range(len(versions)):
        versions2[v] = 'v' + versions[v]
        vList = list(versions2[v])
        if '.' in vList:
            iDot = vList.index('.')
            vList[iDot] = '_'
            versions2[v] = ''.join(vList)
    return versions2


def diffFromBase(versions, elevData):
    # Find the difference between the base model (first in the list) data and the current model version data
    diffElevData = {}
    for v in range(1,len(versions)):
        for k in elevData.keys():
            if not (k in diffElevData):
                diffElevData[k] = {}
            diffElevData[k][versions[v]] = elevData[k][versions[v]] - elevData[k][versions[0]]
    return diffElevData


def writeToCSV(writeData, diffData, filePath, versions):
    outFileName = filePath + "all_max_stages.csv"
    print("Writing to CSV file " + outFileName + "...")
    if os.path.isfile(outFileName):
        os.remove(outFileName)
    header = ['River', 'Reach', 'StationID']
    versionsStr = removePeriod(versions)
    header.extend(versionsStr)
    for v in range(1,len(versionsStr)):
        header.append(versionsStr[v] + "-" + versionsStr[0])
    # Write to a CSV file for further analysis or viewing in Excel
    with open(outFileName, 'wb') as output:
        writer = csv.writer(output)
        writer.writerow(header)
        for k in writeData.keys():
            stationList, stationAddress = filterStations(filePath)
            if k in stationList:
                writeMe = splitKey(stationAddress[k])
                for v in versions:
                    writeMe.append(writeData[k][v])
                for v in range(1,len(versions)):
                        writeMe.append(diffData[k][versions[v]])
                writer.writerow(writeMe)
            else:
                pass


def getPeak(versions, filePath):
    # Reads data from a text file created in getPeakData.py
    print("Reading peak flow data from text file...")
    elevData = {}
    for v in versions:
        dataFileElev = "peakElev_V" + v + ".txt"
        tempData = readFromFile(filePath, dataFileElev)
        tempData = reassignKeys(tempData)
        for k in tempData.keys():
            if not (k in elevData):
                elevData[k] = {}
            elevData[k][v] = tempData[k]
    diffElevData = diffFromBase(versions, elevData)
    writeToCSV(elevData, diffElevData, filePath, versions)

# Used to look at state of variables for debugging
print('makeMaxWselCsv.py is done running.')

def main():
    getData()
    config = CompareConfig()
    getPeak(config.versions, config.filePath)

if __name__ == '__main__':
    main()
