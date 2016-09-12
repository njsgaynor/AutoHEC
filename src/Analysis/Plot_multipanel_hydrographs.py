# Python 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date last updated: March 2016

# This program takes FLOW data from the HEC-RAS model and plots hydrographs from
# multiple model versions on the same axes. User also specifies via input file
# which cross sections to plot.

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
    call(["HEC-DSSVue.cmd", "-s", scriptPath + "getMultiplotData.py"], shell=True)
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
    """Reassigns dict keys to the format used in the HEC models and discards interpolated
    cross sections"""
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


def plotLines(filePath, plotData, k1, labels, versions, fn, vDesc):
    """Plots lines from multiple model versions to the same axis."""
    pyplot.ioff()
    lineColors = ['Black', 'DodgerBlue', 'Coral', 'SeaGreen', 'SaddleBrown']
    lineStyles = ['-', '--', ':', '-.', ':']
    lineWidths = [1, 2, 2, 2, 2]
    figName = "multipanel_hydro" + versions[0] + versions[1] + versions[2] + str(fn)
    f, (ax1, ax2) = pyplot.subplots(2, sharex=True, sharey=True)
    timeToPlot = [0]
    timeToPlot.extend([(float(x)/48.0) for x in range(1,len(plotData[versions[0]][k1[0]]))])
    # print(plotData[versions[v]][k2])
    handles = list(k1)
    for k2 in k1:
        v = 0
        print(k1.index(k2),v)
        print(len(lineColors),len(lineStyles),len(lineWidths),len(plotData),len(plotData[versions[v]]))
        handles[k1.index(k2)], = ax1.plot(timeToPlot,
                                          plotData[versions[v]][k2],
                                          c=lineColors[k1.index(k2)],
                                          ls=lineStyles[v],
                                          lw=lineWidths[v],
                                          Label=labels[k1.index(k2)])
        ax2.plot(timeToPlot, plotData[versions[v]][k2], c=lineColors[k1.index(k2)], ls=lineStyles[v],
                 lw=lineWidths[v])
        v = 1
        ax1.plot(timeToPlot, plotData[versions[v]][k2], c=lineColors[k1.index(k2)], ls=lineStyles[v],
                 lw=lineWidths[v])
        v = 2
        ax2.plot(timeToPlot, plotData[versions[v]][k2], c=lineColors[k1.index(k2)], ls=lineStyles[v],
                 lw=lineWidths[v])
    ax1.legend(handles, labels, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, borderaxespad=0., fancybox=True, framealpha=0.5, frameon=False, mode="expand", fontsize=10) #ncol=len(versions),
    pyplot.subplots_adjust(top=0.8)
    ax1.set_ylabel('Discharge (cfs)', fontsize='10')
    ax2.set_ylabel('Discharge (cfs)', fontsize='10')
    ax1.set_xlim([0,2])
    ax2.set_xlim([0,2])
    pyplot.xlabel('Time in days', fontsize='10')
    ax1.grid(True, color='LightGrey', linestyle=':', linewidth=0.5)
    ax2.grid(True, color='LightGrey', linestyle=':', linewidth=0.5)
    ax1.tick_params(axis='both', which='both', width=0, labelsize=10)
    ax2.tick_params(axis='both', which='both', width=0, labelsize=10)
    ax1.text(0.95, 0.95, vDesc[1],
            verticalalignment='top', horizontalalignment='right',
            transform=ax1.transAxes, fontsize=10)
    ax2.text(0.95, 0.95, vDesc[2],
             verticalalignment='top', horizontalalignment='right',
             transform=ax2.transAxes, fontsize=10)
    ax1.text(1.0, 1.3, 'solid lines:   0% development\ndashed lines: 15% development\ndotted lines: 40% development',
                fontsize='10', verticalalignment='top', horizontalalignment='right', transform=ax1.transAxes)
    pyplot.title('', y=1.18) # vDesc
    pyplot.savefig(filePath + figName + ".png")
    pyplot.close("all")


def getListFromFile(filePath, fileName):
    with open(filePath + fileName, 'rb') as infile:
        inline = list(infile)
    for i in range(len(inline)):
        inline[i] = inline[i].strip('\r\n')
    klist = [[]]
    j = 0
    for i in inline:
        if not i=='':
            klist[j].append(i)
        else:
            klist.append([])
            j += 1
    return klist


def getFlow(versions, filePath, vDesc):
    print("getFlow")
    dataFile = "multipanel_plot_data.txt"
    flowData = readFromFile(filePath, dataFile)
    keylist = getListFromFile(filePath, "multipanel_plot_data_addresses.txt")
    labelList = getListFromFile(filePath, "multipanel_plot_data_labels.txt")
    for k in keylist:
        fn = keylist.index(k)
        l = labelList[keylist.index(k)]
        print(l)
        print(k)
        plotLines(filePath, flowData, k, l, versions, fn, vDesc)

# Used to look at state of variables for debugging
print('done')

def main():
    getData()
    config = CompareConfig()
    getFlow(config.versions, config.filePath, config.vDescription)

if __name__ == '__main__':
    main()
