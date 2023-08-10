import os
import numpy as np

def calc_Ta(filename):
    #reads data and calculates aperture temperature
    #input: calibrated data file from 20m lowres on/off scan of a point source
    #output: mean Ta, std Ta, observation frequency
    #NOTE: Only reads power data from XX column (because YY data was bad)
    
    #_power arrays sum recorded powers
    on_power = []
    off_power = []
    #_count arrays count number of data points for each scan (so we can calculate an average)
    on_count = []
    off_count = []

    with open(filename) as f:
        reading_data = False
        for line in f:
            if "OBSFREQ" in line:
                center_freq = float(line.split("=")[-1]) / 1000
            if "ELEV(deg)" in line:
                elevation = float(line.split("=")[-1])
            #all parameter lines at top of file start with #
            if line[0] == "#":
                continue
            else:
                row = line.split()
                #if row[9] isn't 1, it is a bad data point (either calibration or sweep)
                if row[9] != '1':
                    continue
                cycle = int(int(row[8]) / 2)
                power = float(row[6])
                if row[10] == "on":
                    on = True
                else:
                    on = False

                if on:
                    if len(on_power) < cycle+1:
                        on_power.append(power)
                        on_count.append(1)
                    else:
                        on_power[cycle] += power
                        on_count[cycle] += 1
                else:
                    if len(off_power) < cycle+1:
                        off_power.append(power)
                        off_count.append(1)
                    else:
                        off_power[cycle] += power
                        off_count[cycle] += 1

    on_power_avg = np.divide(on_power,on_count)
    off_power_avg = np.divide(off_power,off_count)
    aperture_temps = np.subtract(on_power_avg,off_power_avg)
    A = 1/(np.sin(elevation*180/np.pi)) #approximation valid for elev > 15 deg
    correction = np.exp(A*0.01) #assumes tau = 0.01
    corrected_aperture_temps = aperture_temps * correction
    
    return np.mean(corrected_aperture_temps), np.std(corrected_aperture_temps), center_freq