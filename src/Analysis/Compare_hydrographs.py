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
    call(["HEC-DSSVue.cmd", "-s", scriptPath + "getFlowData.py"], shell=True)
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
    for key in keyList:
        # Extract station ID from data address in DSS file
        u = key.split('/')
        # Station ID needs to be greater than zero and numeric
        # * indicates interpolated station, letters indicate possible structure, 0.0 is origin station
        try:
            if(float(u[2]))>0:
                x = float(u[2])
                u[2] = roundSigfigs(float(u[2]), 7)  # eight characters/seven sig figs allowed
                newKey = " ".join(u[1:3])  # river/reach + stationID
                dataDict[newKey] = dataDict.pop(key)
            else:
                print("Popping " + key)
                dataDict.pop(key)
        except ValueError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
            print("ValueError:", key)
            dataDict.pop(key)
        except KeyError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
            print("KeyError:", key)
            dataDict.pop(key)
    return dataDict


def plotLines(filePath, plotData, figName, versions):
    pyplot.ioff()
    pyplot.figure(1)
    lineColors = ['b-.', 'r--', 'k:', 'c-', 'm-']
    lineWidths = [2, 1, 2, 1, 1]
    plotLine = versions[:]
    for v in range(len(versions)):
        plotLine[v], = pyplot.plot(range(len(plotData[versions[v]][figName])),
                                   plotData[versions[v]][figName], lineColors[v],
                                   lw=lineWidths[v], Label=versions[v])
    pyplot.legend(plotLine, versions)
    #pyplot.legend(handles=[manualLine, autoLine])
    pyplot.ylabel('Flow (cfs)')
    pyplot.xlabel('Time Step')
    pyplot.title(figName + " V" + versions[0])
    pyplot.savefig(filePath + figName + "_V" + versions[0] + "_hydro.png")
    pyplot.close("all")


def getFlow(versions, filePath):
    print("getFlow")
    flowData = {}
    for v in versions:
        dataFile = "hydrograph_V" + v + ".txt"
        flowData[v] = readFromFile(filePath, dataFile)
        flowData[v] = reassignKeys(flowData[v])
    keylist = flowData[versions[0]].keys()
    for k in keylist:
        plotLines(filePath, flowData, k, versions)

# Used to look at state of variables for debugging
print('done')

def main():
    getData()
    config = CompareConfig()
    getFlow(config.versions, config.filePath)

if __name__ == '__main__':
    main()
