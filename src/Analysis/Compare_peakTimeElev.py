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

def writePeakDiff(outFile, flowDiff):
    print("Writing difference data to CSV file " + outFile + "...")
    if(os.path.isfile(outFile)):
        os.remove(outFile)
    else:
        # Write overflow to a CSV file for further analysis or viewing in Excel
        with open(outFile, 'wb') as output:
            writer = csv.DictWriter(output, [key, values])
            writer.writerows(flowDiff)

def getPeak(bVersions, cVersions, filePath, runName):
    print("Reading peak flow data from text file...")
    peakDiff = {}
    for v in range(len(bVersions)):
        bV = bVersions[v]
        cV = cVersions[v]
        dataFileManualElev = "peakElev_V" + bV + ".txt"
        dataFileAutoElev = "peakElev_V" + cV + ".txt"
        dataFileManualTime = "peakTime_V" + bV + ".txt"
        dataFileAutoTime = "peakTime_V" + cV + ".txt"
        # Loads flow data from manual and automated versions, stored as dict
        dataManualElev = pickle.load(open(filePath + dataFileManualElev, 'rb'))
        dataAutoElev = pickle.load(open(filePath + dataFileAutoElev, 'rb'))
        dataManualTime = pickle.load(open(filePath + dataFileManualTime, 'rb'))
        dataAutoTime = pickle.load(open(filePath + dataFileAutoTime, 'rb'))
        keyList = dataManualElev.keys()
        plotmeManualElev = []
        plotmeManualTime = []
        plotmeAutoElev = []
        plotmeAutoTime = []
        plotmeDiffElev = []
        plotmeDiffTime = []
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
                    newKey = "/" + "/".join(u[1:3])  # river/reach
                    figName = " ".join(u[1:3])
                    plotmeManualElev.append(dataManualElev[newKey + "/LOCATION-ELEV//MAX STAGE/" + runName + "/"])
                    plotmeManualTime.append(dataManualTime[newKey + "/LOCATION-TIME//MAX STAGE/" + runName + "/"])
                    plotmeAutoElev.append(dataAutoElev[newKey + "/LOCATION-ELEV//MAX STAGE/" + runName + "/"])
                    plotmeAutoTime.append(dataAutoTime[newKey + "/LOCATION-TIME//MAX STAGE/" + runName + "/"])
                    diffElev = dataAutoElev[newKey + "/LOCATION-ELEV//MAX STAGE/" + runName + "/"] - \
                               dataManualElev[newKey + "/LOCATION-ELEV//MAX STAGE/" + runName + "/"]
                    plotmeDiffElev.append(diffElev)
                    diffTime = dataAutoTime[newKey + "/LOCATION-TIME//MAX STAGE/" + runName + "/"] - \
                               dataManualTime[newKey + "/LOCATION-TIME//MAX STAGE/" + runName + "/"]
                    plotmeDiffTime.append(diffTime)
                    if (abs(diffElev) > 0.1):
                        print("WSEL >0.1 ft different: " + newKey +  "(" + str(diffElev) + ")")
                    #if (abs(diffTime) > 0.5):
                    #    print("Peak time >0.5 hr different: " + newKey +  "(" + str(diffTime) + ")")
                else:
                    pass
            except ValueError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
                print("ValueError:", key)
            except KeyError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
                print("KeyError:", key)
        # Write diff data to CSV file
        #writeFlowDiff("hydrograph_" + i + ".csv", flowDiff)
        plotScatter(plotmeManualTime, plotmeManualElev, plotmeAutoTime, plotmeAutoElev,
                    plotmeDiffTime, plotmeDiffElev, bV, cV, filePath)
    pass

def plotScatter(dataManualX, dataManualY, dataAutoX, dataAutoY, dataDiffX, dataDiffY, bV, cV, filePath):
    print("Plotting V" + bV + " - V" + cV + "...")
    pyplot.ioff()
    pyplot.figure(1)
    pyplot.scatter(dataManualX, dataManualY, c='blue')
    pyplot.scatter(dataAutoX, dataAutoY, c='red')
    pyplot.figure(2)
    pyplot.scatter(dataDiffX, dataDiffY, c='green')
    pyplot.axis([-3, 3, -1.5, 1.5])
    pyplot.grid(True)
    pyplot.title('V' + bV + " - V" + cV)
    pyplot.xlabel('Delta Peak Time (h)')
    pyplot.ylabel('Delta WSEL (ft)')
    #pyplot.show()
    pyplot.savefig(filePath + "WSELvTIME_V" + bV + " - V" + cV + "_WSEL_TIME.png")
    pyplot.close("all")

# Used to look at state of variables for debugging
print('Compare_peakTimeElev.py is done running.')

def main():
    getData()
    config = CompareConfig()
    getPeak(config.baseVersions, config.compareVersions, config.filePath, config.rasRunName)

if __name__ == '__main__':
    main()
