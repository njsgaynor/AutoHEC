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
import matplotlib.pyplot as pyplot
import HEC_Inundation

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


def readFromCSV(filePath, fileName):
    dataDict = {}
    dataDict['depth'] = {}
    dataDict['time'] = {}
    with open(filePath + fileName, 'rb') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',')
        r = 0
        for row in fileReader:
            if (not r==0):
                dataDict['depth'][' '.join(row[0:2])] = row[2]
                for n in range(len(row[3:])):
                    row[n+3] = float(row[n+3])
                dataDict['time'][' '.join(row[0:2])] = sum(row[3:])
            else:
                r = 1
    return dataDict


def findDiff(baseData, compareData):
    keyList = baseData.keys()
    diffData = {}
    for key in keyList:
        print(compareData[key], baseData[key])
        if (compareData[key]=='-1') and (baseData[key]=='-1'):
            diffData[key] = [0, 1]
            print('both')
        elif compareData[key]=='-1':
            diffData[key] = [float(compareData[key]) - float(baseData[key]) + 1, 3]
            print('compare')
        elif baseData[key]=='-1':
            diffData[key] = [float(compareData[key]) - float(baseData[key]) - 1, 2]
            print('base')
        else:
            diffData[key] = [float(compareData[key]) - float(baseData[key]), 0]
        # if (abs(diffData[key][0]) > 0.1) and dataType=="depth":
        #     print("Depth >0.1 ft different: " + key +  "(" + str(diffData[key]) + ")")
        # elif (abs(diffData[key][0]) > 0.5) and dataType=="time":
        #     print("Time >0.5 hr different: " + key +  "(" + str(diffData[key]) + ")")
    return diffData


def getPeak(versions, filePath, savePath, watershed, timestep):
    print("Reading peak flow data from text file...")
    timeDiff = {}
    depthDiff = {}
    inundData = {}
    for v in versions:
        #HEC_Inundation.main(v)
        dataFileName = "OOB_" + watershed + "_V" + v + ".csv"
        inundData[v] = readFromCSV(filePath, dataFileName)
    for v in versions[1:]:
        depthDiff[v] = findDiff(inundData[versions[0]]['depth'], inundData[v]['depth'])
        timeDiff[v] = findDiff(inundData[versions[0]]['time'], inundData[v]['time'])
    plotScatter(timeDiff, depthDiff, versions, savePath, timestep)


def plotScatter(dataX, dataY, versions, filePath, timestep):
    pyplot.ioff()
    pyplot.figure(1)
    dotColors = ['b', 'r', 'g', 'm', 'k']
    markerTypes = ['o', 'v', '^', 's', '*']
    diffTypes = ['diff', 'bc0', 'b0', 'c0']
    dottyPlots = versions[1:]
    dataX2plot = []
    dataY2plot = []
    dataColor = []
    dataMarkers = []
    for v in range(1, len(versions)):
        for k in dataX[versions[v]].keys():
            dataX2plot.append(float(dataX[versions[v]][k][0])*(timestep/60))
            dataY2plot.append(dataY[versions[v]][k][0])
            dataColor.append(dotColors[dataY[versions[v]][k][1]])
            dataMarkers.append(markerTypes[dataY[versions[v]][k][1]])
        print(v, versions[v])
        print(dataColor)
        for i in range(len(dataX2plot)):
            #dottyPlots[v-1],  = \
            pyplot.scatter(dataX2plot[i], dataY2plot[i], c=dataColor[i], linewidth=0, alpha=0.3) #marker=dataMarkers,
        #pyplot.legend(dottyPlots, diffTypes, scatterpoints=1, loc='upper right')

        #pyplot.axis([-3, 3, -1.5, 1.5])
        pyplot.grid(True)
        #pyplot.title("OOB depth vs OOB time V" + versions[0])
        pyplot.xlabel('Delta OOB Time (hours)')
        pyplot.ylabel('Delta OOB depth (ft)')
        pyplot.savefig(filePath + "OOB_DvT_V" + versions[v] + "-V" + versions[0] + "_OOB.png")
        pyplot.close("all")

# Used to look at state of variables for debugging
print('Compare_Inundation.py is done running.')

def main():
    #getData()
    config = CompareConfig()
    getPeak(config.versions, config.filePath, config.filePath, config.watershed, config.timestep)

if __name__ == '__main__':
    main()
