import sys
import time

from datetime import datetime
import ephem
import matplotlib.pyplot as plt
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital
import urllib

example_script_input = f'IAC80 "STARLINK-1436 (VISORSAT)" 2020 8 31'
observatories= {
    'KPEAK':['K.P. Observatory', +31.9599, -111.5997, 2.067],
    'CTIO':['CTIO', -30.1690, -70.8063, 2.2],
    'CKOIRAMA':['Ckoirama Observatory', -24.08913333, -69.93058889, 0.966],
    'HOME':['Home', +32.2671111, -110.8507778, .753],
    'VLT':['VLT', -24.6275, -70.4044, 2.650],
    'VISTA':['VISTA', -24.6157000, -70.3976000, 2.635],
    'CHILESCOPE':['CHILESCOPE', -30.4708333333333, -70.7647222222222, 1.580],
    'IAC80':['IAC80', +28.29966667, -16.51102778, 2.38125],
    'CA':['CA', 37.22364444, -2.54621667, 2.168]
    }
################################################################################
def input_handler(arguments):

    "arguments: list with arguments pass to the script"

    n_args = len(arguments)

    if n_args < 6:
        print(f'Use: python satellite_track.py OBSname SATid Year Month Day')
        print(f'Ex: python satellite_track.py {example_script_input}')
        sys.exit()

    elif arguments[1] in observatories.keys():

        obs_name = observatories[arguments[1]][0]
        obs_lat = observatories[arguments[1]][1]
        obs_lon = observatories[arguments[1]][2]
        obs_altitude = observatories[arguments[1]][3]
        satellite_ID = arguments[2]
        satellite_brand = satellite_ID.split('-')[0].lower()
        year  = int(arguments[3])
        month = int(arguments[4])
        day   = int(arguments[5])

        return (obs_name, obs_lat, obs_lon, obs_altitude, year, month, day,
            satellite_ID, satellite_brand)

    else:

        print(f'Observatory name = {arguments[1]}  not found...')
        sys.exit()
################################################################################
def radians_to_deg(radians):

    deg = radians*180./np.pi

    if deg < 0:
           deg += 360

    return deg

def radians_to_hrs(radians):

    deg = radians_to_deg(radians)

    hrs = deg*24./360

    return hrs

def radians_to_hh_mm_ss(radians):

    # converts the RA to hh:mm:ss.sss

    hrs = radians_to_hrs(radians)
    hh = int(hrs)

    mins = (hrs-hh)*60.
    mm = int(mins)

    ss = (mins-mm)*60

    return hh, mm, ss

def dec_to_dd_mm_ss(dec):
    # converts the DEC to dd:mm:ss

    if dec < 0:
       dec_sign = -1
       dec = abs(dec)
    else:
        dec_sign = 1

    dd, mm, ss = radians_to_hh_mm_ss(radians=dec)

    return dd, mm, ss
################################################################################
