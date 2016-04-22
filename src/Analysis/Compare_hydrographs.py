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
    # Path to scritp that extracts data from DSS file
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

def writeFlowDiff(outFile, flowDiff):
    print("writeFlowDiff")
    if(os.path.isfile(outFile)):
        os.remove(outFile)
    else:
        # Write overflow to a CSV file for further analysis or viewing in Excel
        with open(outFile, 'wb') as output:
            writer = csv.DictWriter(output, [key, values])
            writer.writerows(flowDiff)

def getFlow(bVersions, cVersions, filePath):
    print("getFlow")
    flowDiff = {}
    for v in range(len(bVersions)):
        bV = bVersions[v]
        cV = cVersions[v]
        dataFileManual = "hydrograph_V" + bV + ".txt"
        dataFileAuto = "hydrograph_V" + cV + ".txt"
        # Loads flow data from manual and automated versions, stored as dict
        flowDataManual = pickle.load(open(filePath + dataFileManual, 'rb'))
        flowDataAuto = pickle.load(open(filePath + dataFileAuto, 'rb'))
        keyList = flowDataManual.keys()
        # Calculate difference between auto and manual versions
        #for k in keyList:
        #    flowDiff[k] = map(operator.sub, flowDataAuto[k], flowDataManual[k])
        # Get rid of interpolated stations
        for key in keyList:
            # Extract station ID from data address in DSS file
            u = key.split('/')
            # Station ID needs to be greater than zero and numeric
            # * indicates interpolated station, letters indicate possible structure, 0.0 is origin station
            try:
                if(float(u[2]))>0:
                    x = float(u[2])
                    u[2] = roundSigfigs(float(u[2]), 7)  # eight characters/seven sig figs allowed
                    figName = " ".join(u[1:3])  # river/reach
                    #print(flowDataAuto[key])
                    #print(flowDataManual[key])
                    #flowDiff[newKey] = map(operator.sub, flowDataAuto.pop(key), flowDataManual.pop(key))
                    #print(flowDiff)
                    plotFlow(flowDataManual[key], flowDataAuto[key], figName, bV, cV, filePath)
                    #time.sleep(2.0)
                else:
                    pass
            except ValueError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
                print("ValueError:", key)
            except KeyError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
                print("KeyError:", key)
        # Write diff data to CSV file
        #writeFlowDiff("hydrograph_" + i + ".csv", flowDiff)
        pass

def plotFlow(soDataManual, soDataAuto, figName, bV, cV, filepath):
    pyplot.ioff()
    manualLine, = pyplot.plot(soDataManual, 'b-', lw=2, Label=bV)
    autoLine, = pyplot.plot(soDataAuto, 'r-', Label=cV)
    pyplot.legend(handles=[manualLine, autoLine])
    pyplot.ylabel('Flow (cfs)')
    pyplot.xlabel('Time Step')
    pyplot.title(figName + " V" + bV + " - V" + cV)
    #pyplot.show()
    pyplot.savefig(filepath + figName + "_V" + bV + " - V" + cV + "_hydro.png")
    pyplot.close("all")

# Used to look at state of variables for debugging
print('done')

def main():
    getData()
    config = CompareConfig()
    getFlow(config.baseVersions, config.compareVersions, config.filePath)

if __name__ == '__main__':
    main()
