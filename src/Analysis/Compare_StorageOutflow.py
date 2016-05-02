# Python 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date last updated: May 2016

# This program takes STORAGE-OUTFLOW data from the HEC-RAS model and plots the
# curves from different versions on a single graph for each subbasin.

import math
from Compare_Config import CompareConfig
from subprocess import call
import pickle
import os
import matplotlib.pyplot as pyplot

def getData():
    """Get data from a DSS file"""
    popd=os.getcwd()
    dssvuePath = "C:/Program Files (x86)/HEC/HEC-DSSVue/"
    os.chdir(dssvuePath)
    # Path to scritp that extracts data from DSS file
    scriptPath = "C:/Users/nschiff2/IdeaProjects/AutoHEC/src/Analysis/"
    # Use HEC-DSSVue to run script (only way to use hec package that accesses DSS files)
    call(["HEC-DSSVue.cmd", "-s", scriptPath + "getSOData.py"], shell=True)
    os.chdir(popd)

def roundSigfigs(num, sigfigs):
    """Round to specified number of sigfigs.
    from http://code.activestate.com/recipes/578114-round-number-to-
    specified-number-of-significant-di/
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
        t = key.split('/')
        u = t[2].split('_')
        if (len(u[0]) > 1):
            try:
                float(u[1])
                newKey = u[0]
            except Exception, e:
                if (len(u) > 1):
                    newKey = u[0] + "_" + u[1]
                    print("Key too short, using longer key: " + newKey)
                else:
                    newKey = u[0]
                    print("Key too short, using longer key: " + newKey)
        else:
            newKey = u[0] + "_" + u[1]
            print("Key too short, using longer key:" + newKey)
        dataDict[newKey] = dataDict.pop(key)
    return dataDict


def plotLines(filePath, plotData, figName, versions):
    pyplot.ioff()
    pyplot.figure(1)
    lineColors = ['b-.', 'r--', 'k:', 'c-', 'm-']
    lineWidths = [2, 1, 2, 1, 1]
    plotLine = versions[:]
    for v in range(len(versions)):
        try:
            plotLine[v], = pyplot.plot(plotData[versions[v]][figName][0],
                                       plotData[versions[v]][figName][1], lineColors[v],
                                       lw=lineWidths[v], Label=versions[v])
        except KeyError:
            print("Key not found in V" + versions[v] + ": " + figName)
    pyplot.legend(plotLine, versions)
    #pyplot.legend(handles=[manualLine, autoLine])
    pyplot.ylabel('Discharge (cfs)')
    pyplot.xlabel('Storage (ac-ft)')
    pyplot.title(figName + " V" + versions[0])
    try:
        pyplot.savefig(filePath + figName + "_V" + versions[0] + "_SO.png")
    except Exception, e:
        print(str(e))
    pyplot.close("all")


def getSO(versions, filePath):
    print("Reading storage-outflow data from text files...")
    soData = {}
    for v in versions:
        dataFile = "storageoutflow_V" + v + ".txt"
        soData[v] = readFromFile(filePath, dataFile)
        soData[v] = reassignKeys(soData[v])
    keylist = soData[versions[0]].keys()
    print("Plotting storage-outflow data...")
    for k in keylist:
        plotLines(filePath, soData, k, versions)

# Used to look at state of variables for debugging
print('done')

def main():
    getData()
    config = CompareConfig()
    getSO(config.versions, config.filePath)

if __name__ == '__main__':
    main()
