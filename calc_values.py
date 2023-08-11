import os
import numpy as np


def calc_Ta_obs(filename):
    # reads data and calculates aperture temperature
    # input: calibrated data file from 20m lowres on/off scan of a point source
    # output: mean Ta, std Ta, observation center frequency
    # NOTE: Only reads power data from XX column (because YY data was bad)

    # _power arrays sum recorded powers
    on_power = []
    off_power = []
    # _count arrays count number of data points for each scan (so we can calculate an average)
    on_count = []
    off_count = []

    # with open(filename) as f:
    f = filename.readlines()
    reading_data = False
    for line in f:
        line = line.decode()
        if "OBSFREQ" in line:
            center_freq = float(line.split("=")[-1]) / 1000
        if "ELEV(deg)" in line:
            elevation = float(line.split("=")[-1])
        # all parameter lines at top of file start with #
        if line[0] == "#":
            continue
        else:
            row = line.split()
            # if row[9] isn't 1, it is a bad data point (either calibration or sweep)
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

    on_power_avg = np.divide(on_power, on_count)
    off_power_avg = np.divide(off_power, off_count)
    antenna_temps = np.subtract(on_power_avg, off_power_avg)
    # approximation valid for elev > 15 deg
    A = 1/(np.sin(elevation*np.pi/180))
    correction = np.exp(A*0.01)  # assumes tau = 0.01
    corrected_antenna_temps = antenna_temps * correction
    return np.mean(corrected_antenna_temps), np.std(corrected_antenna_temps), center_freq


def calc_S(center_freq, coeffs):
    # calculate flux
    # assumes flux can be calculated with a polynomial as in:
    # https://iopscience.iop.org/article/10.3847/1538-4365/aa6df9/pdf
    logS = 0
    logV = np.log10(center_freq)
    for i, a in enumerate(coeffs):
        logS += a * logV**i
    return 10**logS
