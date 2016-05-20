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
import operator
import matplotlib.pyplot as pyplot
import time

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


def findDiff(baseData, compareData, dataType):
    keyList = baseData.keys()
    diffData = {}
    # Get rid of interpolated stations
    for key in keyList:
        diffData[key] = compareData[key] - baseData[key]
        if (abs(diffData[key]) > 0.1) and dataType=="Elev":
            print("WSEL >0.1 ft different: " + key +  "(" + str(diffData[key]) + ")")
    return diffData


def reassignKeys(dataDict):
    keyList = dataDict.keys()
    # Get rid of interpolated stations
    for key in keyList:
        # Extract station ID from data address in DSS file
        u = key.split('/')
        # Station ID needs to be greater than zero and numeric
        # * indicates interpolated station, letters indicate possible structure, 0.0 is origin station
        try:
            if(float(u[2]))>0:
                u[2] = roundSigfigs(float(u[2]), 7)  # eight characters/seven sig figs allowed
                newKey = "/" + "/".join(u[1:3])  # river/reach
                dataDict[newKey] = dataDict.pop(key)# + dataAddress + runName + "/")
            else:
                print("Popping " + key)
                dataDict.pop(key)# + dataAddress + runName + "/")
        except ValueError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
            print("ValueError:", key)
    return dataDict


def getPeak(versions, filePath):
    print("Reading peak flow data from text file...")
    elevDiff = {}
    timeDiff = {}
    elevData = {}
    timeData = {}
    for v in versions:
        dataFileElev = "peakElev_V" + v + ".txt"
        dataFileTime = "peakTime_V" + v + ".txt"
        elevData[v] = readFromFile(filePath, dataFileElev)
        timeData[v] = readFromFile(filePath, dataFileTime)
        elevData[v] = reassignKeys(elevData[v])
        timeData[v] = reassignKeys(timeData[v])
    for v in versions[1:]:
        elevDiff[v] = findDiff(elevData[versions[0]], elevData[v], "Elev")
        timeDiff[v] = findDiff(timeData[versions[0]], timeData[v], "Time")
    plotScatter(timeDiff, elevDiff, versions, filePath)


def plotScatter(dataX, dataY, versions, filePath):
    pyplot.ioff()
    pyplot.figure(1)
    dotColors = ['b', 'r', 'c', 'm', 'k']
    markerTypes = ['o', 'v', '^', 's', '*']
    dottyPlots = versions[1:]
    print(len(dottyPlots))
    for v in range(1, len(versions)):
        print(v, versions[v])
        dottyPlots[v-1] = pyplot.scatter(dataX[versions[v]].values(), dataY[versions[v]].values(), c=dotColors[v-1],
                                         marker=markerTypes[v-1], linewidth=0, alpha=0.5)
    pyplot.legend(dottyPlots, versions[1:], scatterpoints=1, loc='upper right')
    pyplot.axis([-3, 3, -1.5, 1.5])
    pyplot.grid(True)
    pyplot.title("WSEL vs TIME V" + versions[0])
    pyplot.xlabel('Delta Peak Time (h)')
    pyplot.ylabel('Delta WSEL (ft)')
    pyplot.savefig(filePath + "WSELvTIME_V" + versions[0] + "_WSEL_TIME.png")
    pyplot.close("all")

# Used to look at state of variables for debugging
print('Compare_peakTimeElev.py is done running.')

def main():
    getData()
    config = CompareConfig()
    getPeak(config.versions, config.filePath, config.rasRunName)

if __name__ == '__main__':
    main()
