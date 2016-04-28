# Python 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date last updated: March 2016

# This program takes data from the HEC-RAS model and compares the max stage and hourly stage to the bank station
# elevations to determine how far out of banks the water rises and how many hours the water is out of banks. This is
# recorded for each out-of-banks event in the simulation. Output is to a CSV file with columns RiverReach, StationID,
# and OOB_Depth#, and OOB_Time# for each OOB event (numbered #). **When preparing the bank station elevations file,
# do not include Node Names in the table (under Options menu in the Profile Output Table of HEC-RAS).**

import csv
import math
from HEC_Inundation_Config import BankStation_config
from subprocess import call
import pickle
import os

def getData():
    """Get data from a DSS file"""
    print("getData")
    popd=os.getcwd()
    dssvuePath = "C:/Program Files (x86)/HEC/HEC-DSSVue/"
    os.chdir(dssvuePath)
    # Path to scritp that extracts data from DSS file
    scriptPath = "C:/Users/nschiff2/IdeaProjects/AutoHEC/src/Analysis/"
    # Use HEC-DSSVue to run script (only way to use hec package that accesses DSS files)
    print("HEC-DSSVue.cmd", "-s", scriptPath + "getStageData.py")
    call(["HEC-DSSVue.cmd", "-s", scriptPath + "getStageData.py"], shell=True)
    os.chdir(popd)

def roundSigfigs(num, sigfigs):
    """Round to specified number of sigfigs.
    from http://code.activestate.com/recipes/578114-round-number-to-specified-number-of-significant-di/
    accessed 3/24/2016"""
    if num != 0:
        return str(round(num, -int(math.floor(math.log10(abs(num))) - (sigfigs - 1))))
    else:
        return str(0.0)  # Can't take the log of 0

def getTimeStage(dataPath):
    print("Reading stage time series data from text file and get rid of interpolated stations...")
    timestage = pickle.load(open(dataPath + "timestage.txt", 'rb'))
    # For every item in timestage (each station in Stony Creek), keep the data only if it is not an interpolated
    # station. The station ID is the second item in the data address.
    keyList = timestage.keys()
    print("Length of stage time series dataset before culling interpolated stations: " + str(len(timestage)))
    for key in keyList:
        # Extract station ID from data address in DSS file
        u = key.split('/')
        # Station ID needs to be greater than zero and numeric
        # * indicates interpolated station, letters indicate possible structure, 0.0 is origin station
        try:
            if(float(u[2]))>0:
                v = float(u[2])
                u[2] = roundSigfigs(float(u[2]), 7)  # eight characters/seven sig figs allowed
                newKey = " ".join(u[1:3])  # river/reach
                timestage[newKey] = timestage.pop(key)
            else:
                timestage.pop(key)
        except ValueError:  # if station ID includes anything but numbers (* is interpolated; letters may be a structure)
            timestage.pop(key)
    return timestage

def getBankElevations(bankFile):
    print("Reading bank elevations data from CSV file and get rid of interpolated stations...")
    # Open CSV file that contains the bank station elevations for each station in the Stony Creek watershed and read whole
    # file into a list.
    #   The CSV was copy-pasted from HEC-RAS (Profile output table) to Excel (data and headers) and saved as a CSV file.
    #   Interpolated cross sections must be included or only four decimal places of the station ID will show. This data is
    #   not available in HEC-DSSVue.
    with open(bankFile, 'rb') as csvfile:
        bank = list(csv.reader(csvfile, delimiter=','))
        print('Length of bank station dataset before culling interpolated stations: ' + str(len(bank)))   #used for debugging
        # For every column in bank (each station in Stony Creek), keep the data only if it is not an interpolated station.
        #   The first three elements are river, reach, and station ID. Station ID needs to be converted to a float.
        #   Then concatenate river and reach into a single, uppercase element and assign to element 1.
        #   Store river/reach, station ID, left bank, and right bank for each station in bank_ID.
        bankDict = {}
        count = 0
        for t in bank:
            t[1] = " ".join(bank[count][0:2])
            t[1] = t[1].upper()
            # Station ID needs to be greater than zero and numeric
            # * indicates interpolated station, letters indicate possible structure, 0.0 is origin station
            try:
                r = float(t[2])
                if r > 0:
                    t[2] = roundSigfigs(float(t[2]), 7)
                    location = " ".join(t[1:3])
                    bankDict.update({location: list(t[-2:])})
            except ValueError:
                pass
            count += 1
        return bankDict

def getMaxStage(timestage, dataPath):
    print("Reading max stage data from text file and get rid of interpolated stations...")
    maxstage = pickle.load(open(dataPath + "maxstage.txt", 'rb'))
    # For every item in maxstage (each station in Stony Creek), keep the data only if it is not an interpolated
    # station. The station ID is the second item in the data address. Timestage is used as the reference standard
    # for which stations to keep.
    keyList = maxstage.keys()
    print("Length of max stage dataset before culling interpolated stations: " +  str(len(maxstage)))
    for key in keyList:
        # Extract station ID from data address in DSS file
        u = key.split('/')
        u[2] = roundSigfigs(float(u[2]), 7)
        newKey = " ".join(u[1:3])  # river/reach
        # Use timestage as the reference standard for which stations should be retained.
        if timestage.has_key(newKey):  # if station ID is not interpolated
            maxstage[newKey] = maxstage.pop(key)
        else:  # if station ID is interpolated
            maxstage.pop(key)
            print("Popping station:", newKey)
    return maxstage

def checkInputs(bank, timestage, maxstage):  # Mainly for debugging
    # Debug which stations don't match between maxstage, bank, and timestage
    for y in maxstage:
        if(not bank.has_key(y)):
            print("Error: No key ", y, " in list of bank stations.")
        if(not timestage.has_key(y)):
            print("Error: No key ", y, " in time series of stage data.")
        #assert bank.has_key(y)
        #assert timestage.has_key(y)
        pass
    # Used to check that each data set has the same number of stations (debugging)
    print('Length of max stage dataset after culling interpolated stations: ' + str(len(maxstage)))
    print('Length of stage time series dataset after culling interpolated stations: ' + str(len(timestage)))
    print('Length of bank station dataset after culling interpolated stations: ' + str(len(bank)))

def match_stations(config):
    timestage = getTimeStage(config.dataPath)
    bank = getBankElevations(config.bankFileName)
    maxstage = getMaxStage(timestage, config.dataPath)
    checkInputs(bank, timestage, maxstage)  # Mainly for debugging
    return maxstage, timestage, bank

def getStationID(item):  # Returns River/Reach separate from station ID number
    temp = item.split(' ')
    return ' '.join(temp[0:(len(temp)-1)]), temp[len(temp)-1]

def OOB_DepthTime(bank, timestage, maxstage):
    print("OOB_DepthTime")
    # By this point maxstage_ID, timestage_ID, and bank_ID should contain all the same stations.
    # River/reach/ID will be checked each time to make sure this is the case. Then calculate how far the max stage
    # exceeds the lower bank station and for how many hours the stage/water surface elevation exceeds the lower bank
    # station.
    overflow = [['River_Reach', 'Station_ID', 'OOB_Depth1', 'OOB_Time1']]
    count = 0
    # For each station
    for item in bank:
        riverReach, stationID = getStationID(item)
        overflow.append([riverReach, stationID])
        overflow[count+1].extend([-1, 0])
        # Calculate the lower bank station, the max stage OOB, and initialize the first OOB event
        lowbank = float(min(bank[item]))
        try:
            OOB_depth = round(float(maxstage[item])-lowbank, 4)
        except KeyError:
            print("Key Error in max stage dataset: ", str(item))
        if (not OOB_depth < 0):
            overflow[count+1][2] = OOB_depth
        else:
            overflow[count+1][2] = -1
        OOB_event = 1
        # For each time recorded at station [item]
        for stage in range(len(timestage[item])):
            if float(timestage[item][stage]) > lowbank:
                try:
                    # Count the number of output times when river is out of banks
                    overflow[count+1][OOB_event+2] += 1
                except IndexError:
                    # If OOB_event just started, add it to the list for current station
                    overflow[count+1].extend([1])
                    # Add column header if it doesn't exist yet
                    try:
                        overflow[0][OOB_event+2]
                    except IndexError:
                        overflow[0].extend(['OOB_Time'+str(OOB_event)])
            elif (float(timestage[item][stage]) < lowbank) and (overflow[count+1][-1] > 0):
                # If within banks after >=1 OOB event, increment event counter
                try:
                    overflow[count+1][OOB_event+2]
                    OOB_event += 1
                except IndexError:
                    pass
        count = count + 1
    return overflow

def writeOOB_DepthTime(outFile, overflow):
    print("Writing out-of-banks depth and time to CSV file " + outFile + "...")
    if(os.path.isfile(outFile)):
        os.remove(outFile)
    else:
        # Write overflow to a CSV file for further analysis or viewing in Excel
        with open(outFile, 'wb') as output:
            writer = csv.writer(output)
            writer.writerows(overflow)

# Used to look at state of variables for debugging
print('HEC_Inundation is done running.')

def main():
    getData()
    config = BankStation_config()
    maxstage, timestage, bank = match_stations(config)
    overflow = OOB_DepthTime(bank, timestage, maxstage)
    writeOOB_DepthTime(config.outFileName, overflow)

if __name__ == '__main__':
    main()
