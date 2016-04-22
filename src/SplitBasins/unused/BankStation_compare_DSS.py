# Python 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date: February 2016

# This program takes data from the HEC-RAS model and compares the max stage and hourly stage to the bank station
# elevations to determine how far out of banks the water rises and how many hours the water is out of banks. This is
# recorded for each out-of-banks event in the simulation. Output is to a CSV file with columns RiverReach, StationID,
# and OOB_Depth#, and OOB_Time# for each OOB event (numbered #).

import sys
sys.path.append("C:/Program Files (x86)/HEC/HEC-DSSVue/jar/hec.jar")
sys.path.append("C:/Program Files (x86)/HEC/HEC-DSSVue/jar/heclib.jar")
sys.path.append("C:/Program Files (x86)/HEC/HEC-DSSVue/jar/hecData.jar")
sys.path.append("C:/Program Files (x86)/HEC/HEC-DSSVue/jar/rma.jar")
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/bin/java.exe")
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/src/java")
sys.path.append("C:/Program Files/Java/javahelp-2.0.05.jar")

import java
import javax.help
import csv
from operator import itemgetter
import hec.script
import hec.heclib.dss

def main():
    get_dss_data()
#    (bank_ID, timestage_ID, maxstage_ID) = match_stations()
#    OOB_DepthTime(bank_ID, timestage_ID, maxstage_ID)


def get_dss_data():
    try:
#        try:
        dssfile = HecDss.open('C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/STCR_Design2.dss',1)
        stage = dssfile.read('/E STONY CR DITCH E STONY CR DITCH//LOCATION-ELEV//MAX STAGE/100YR24HRISWS/')
    except Exception, e:
        MessageBox.showError(' '.join(e.args), 'Python Error')
    except java.lang.Throwable, e:
        MessageBox.showError(e.getMessage(), 'Error')
    finally:
        dssfile.done()
    print('get_dss_data')


def match_stations():
    # Open CSV file that contains the hourly stage data for Stony Creek watershed and read whole file into a list.
    #   The CSV was copy-pasted from HEC-RAS output to Excel (data and headers) and saved as a CSV file. This took
    #   two batches of copying because HEC-RAS can only display up to 500 pathnames at a time. HEC-RAS was used instead
    #   of HEC-DSSVue because HEC-DSSVue does not include the name of the reach and some of the stations had slightly
    #   different numbers in different reaches.
    with open('C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/StonyCreek_timestage3.csv', 'rb') as csvfile:
        timestage = list(csv.reader(csvfile, delimiter=','))
#        print('timestage ',len(timestage[0]))   #used for debugging

        # For every column in timestage (each station in Stony Creek), keep the data only if it is not an interpolated
        # station.
        #   The station ID is at the end of the location string that includes the river, reach, and station ID.
        #   Then assign the extracted station ID to the second row of the matrix/list, overwriting INST-VAL.
        #   Also assign river and reach to first row of matrix/list (essentially deleting the station ID from that element).
        #   Stores as river/reach, ID, and hourly stage data for 72 hours in timestage_ID.
        timestage_ID = []
        count = 0
        # Loop through all columns, looking at the first row to see if the station ID has an asterisk
        for t in timestage[0]:
            # Extract station ID from full location string
            u = t.split()
            if len(u) > 0:
                try:
                    # Station ID is last element of list item, so u[len(u)-1]
                    v = float(u[len(u)-1])
                    timestage[2][count] = v
                    # Reference ranges are non-inclusive on the upper end
                    timestage[1][count] = " ".join(u[0:len(u)-1])
                    z = []
                    for y in timestage:
                        z.append(y[count])
                    if z[2] > 0:
                        timestage_ID.append(z[1:])
                except ValueError:
                    pass
            else:
                # Use this to skip blanks in first two columns
                pass
            count += 1
        # Sort by station ID, then river/reach for matching with other data sets
        timestage_ID.sort(key=itemgetter(1, 0))
        # Delete variables no longer in use
        del timestage   # u, v, y, z could also be deleted

    # Open CSV file that contains the bank station elevations for each station in the Stony Creek watershed and read whole
    # file into a list.
    #   The CSV was copy-pasted from HEC-RAS (Profile output table) to Excel (data and headers) and saved as a CSV file.
    #   Interpolated cross sections must be included or only four decimal places of the station ID will show. This data is
    #   not available in HEC-DSSVue.
    with open('C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/StonyCreek_banks2.csv', 'rb') as csvfile:
        bank = list(csv.reader(csvfile, delimiter=','))
    #    print('bank ',len(bank))   #used for debugging

        # For every column in bank (each station in Stony Creek), keep the data only if it is not an interpolated station.
        #   The first three elements are river, reach, and station ID. Station ID needs to be converted to a float.
        #   Then concatenate river and reach into a single, uppercase element and assign to element 1.
        #   Store river/reach, station ID, left bank, and right bank for each station in bank_ID.
        bank_ID = []
        temp = []   # used to store interpolated station IDs for later use
        count = 0
        for t in bank:
            t[1] = " ".join(bank[count][0:2])
            t[1] = t[1].upper()
            try:
                t[2] = float(t[2])
                if t[2] > 0:
                    bank_ID.append(t[1:])
            except ValueError:
                temp.append(t[1:3])
                pass
            count += 1
        # Sort by station ID, then river/reach for matching with other data sets
        bank_ID.sort(key=itemgetter(1, 0))
        # Delete variables no longer in use
        del bank    # could also delete t

        # Create list of interpolated stations. This is needed to find interpolated stations in maxstage, where the
        # interpolated stations are not marked. Stores river/reach and ID in interp_ID.
        count = 0
        interp_ID = []
        for a in temp:
            a[1] = a[1].strip()
            a[1] = a[1].strip('*')
            try:
                b = float(a[1])
                interp_ID.append([a[0], float(a[1])])
            except ValueError:
                pass
        # Sort for easier searching if need to find things manually
#        interp_ID.sort()
        # Delete variables no longer in use
        del temp    # could also delete a, b

    # Open CSV file that contains the max stage for each station in the Stony Creek watershed and read whole file into a
    # list.
    #   The CSV was copy-pasted from HEC-RAS output to Excel (data and headers), manually condensed into a single sheet with
    #   three columns (river/reach, station ID, max stage), and saved as a CSV file. HEC-RAS was used instead of HEC-DSSVue
    #   because HEC-DSSVue does not include the name of the reach. However, HEC-RAS does not annotate the interpolated cross
    #   sections, so the interpolated river/reach and IDs (interp_ID) were pulled from the bank stations and used to filter
    #   out the interpolated stations. In addition, six decimal places must be used to include the entire station ID for all
    #   stations.
    with open('C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/StonyCreek_maxstage2.csv', 'rb') as csvfile:
        maxstage = list(csv.reader(csvfile, delimiter=','))
#        print('maxstage ',len(maxstage))   #used for debugging

        # For every column in maxstage (each station in Stony Creek), keep the data only if it is not an interpolated
        # station.
        #   The first two elements are river/reach and station ID. Station ID needs to be converted to a float.
        #   Store river/reach, station ID, and max stage for each station in bank_ID.
        maxstage_ID = []
        for t in maxstage:
            t[0] = t[0].strip()
            try:
                t[1] = float(t[1])
                # Station must not be in the list of interpolated stations. Compare river/reach and station ID because each
                # reach has its own IDs (i.e. IDs may not be unique when considering multiple reaches).
                if (t[1] > 0) and (t[0:2] not in interp_ID):
                    maxstage_ID.append(t)
            except ValueError:
                pass
        # Sort by station ID, then river/reach for matching with other data sets
        maxstage_ID.sort(key=itemgetter(1, 0))
        # Delete variables no longer in use
        del maxstage    # could also delete t

    # Debug which stations don't match between maxstage, bank, and timestage
#        count = 0
#        for y in maxstage_ID:
#            if (maxstage_ID[count][1]-bank_ID[count][2])!=0:
#                print(bank_ID[count][2],maxstage_ID[count][1])
#            count += 1

    # Used to check that each data set has the same number of stations (debugging)
#    print('maxstage_ID ',len(maxstage_ID))
#    print('timestage_ID ',len(timestage_ID))
#    print('bank_ID ',len(bank_ID))

    return (bank_ID, timestage_ID, maxstage_ID)


def OOB_DepthTime(bank_ID, timestage_ID, maxstage_ID):
    # By this point maxstage_ID, timestage_ID, and bank_ID should contain all the same stations in the same order.
    # River/reach and ID will be checked each time to make sure this is the case. Then calculate how far the max stage
    # exceeds the lower bank station and for how many hours the stage/water surface elevation exceeds the lower bank
    # station. **This is currently only able to handle a single out-of-banks event.**
    overflow = [['River_Reach', 'Station_ID', 'OOB_Depth1', 'OOB_Time1']]
    # For each station
    for item in range(len(bank_ID)):
        overflow.append(bank_ID[item][0:2])
        overflow[item+1].extend([-1, 0])
        # Double check that the stations match
        ID1 = bank_ID[item][1] == timestage_ID[item][1]
        ID2 = bank_ID[item][1] == maxstage_ID[item][1]
        RR1 = bank_ID[item][0] == timestage_ID[item][0]
        RR2 = bank_ID[item][0:1] == maxstage_ID[item][0:1]
        if ID1 and ID2 and RR1 and RR2:
            lowbank = float(min(bank_ID[item][-2:]))
            OOB_event = 1
            # For each time
            for stage in range(2, len(timestage_ID[item])):
                if float(timestage_ID[item][stage]) > lowbank:
                    try:
                        # Count the number of times when river is out of banks
                        overflow[item+1][(OOB_event*2)+1] += 1
                    except IndexError:
                        overflow[item+1].extend([-1, 0])
                        overflow[0].extend(['OOB_Depth'+str(OOB_event), 'OOB_Time'+str(OOB_event)])
                    # Check if difference between lower bank and stage is larger than the largest difference thus far and
                    # save the larger of the two as the max out of banks.
                    if (float(timestage_ID[item][stage])-lowbank) > overflow[item+1][2]:
                        overflow[item+1][(OOB_event*2)] = round(float(timestage_ID[item][stage])-lowbank, 4)
                elif (float(timestage_ID[item][stage]) < lowbank) and (overflow[item+1][-1] > 0):
                    OOB_event += 1
        else:
            raise Exception('At least one station location does not match (BankStation_compare.py).')

    # Write overflow to a CSV file for further analysis or viewing in Excel
    with open('C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/OOB_StonyCreek.csv', 'wb') as output:
        writer = csv.writer(output)
        writer.writerows(overflow)

# Used to look at state of variables for debugging
#print('done')

if __name__ == '__main__':
    main()
