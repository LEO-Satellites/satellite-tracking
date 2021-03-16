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
observatory_names = {
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
    #   print("Use: python track_sat.py OBSname SATid Year Month Day\nEx:  python track_sat_rev0p7.py IAC80 "STARLINK-1436 (VISORSAT)" 2020 8 31\n")
        print(f'Use: python track_sat.py OBSname SATid Year Month Day')
        print(f'Ex: python track_sat_rev0p7.py {example_script_input}')

    elif arguments[1] in observatory_names.keys():
        obs_name = observatory_names[arguments[1]][0]
        obs_lat = observatory_names[arguments[1]][1]
        obs_lon = observatory_names[arguments[1]][2]
        obs_altitude = observatory_names[arguments[1]][3]
        satellite_ID = arguments[2]
        year  = int(arguments[3])
        month = int(arguments[4])
        day   = int(arguments[5])
        return (obs_name, obs_lat, obs_lon, obs_altitude, year, month, day,
            satellite_ID)
    else:
        print(f'Observatpry name = {arguments[1]}  not found...')


    # else:
    #    OBSname = arguments[1]
    #    if OBSname == "KPEAK":
    #       #Kitt Peak Observatory location
    #       obsName = 'K.P. Observatory'
    #       (obs_lat, obs_lon, obs_altitude) = (+31.9599, -111.5997, 2.067)
    #    elif OBSname == "CTIO":
    #       #CTIO  Observatory location
    #       obsName = 'CTIO'
    #       (obs_lat, obs_lon, obs_altitude) = (-30.1690, -70.8063, 2.2)
    #    elif OBSname == "CKOIRAMA":
    #       #Ckoirama Observatory location
    #       obsName = 'Ckoirama Observatory'
    #       (obs_lat, obs_lon, obs_altitude) = (-24.08913333, -69.93058889, 0.966)
    #    elif OBSname == "HOME":
    #       #home location
    #       obsName = 'Home'
    #       (obs_lat, obs_lon, obs_altitude) = (+32.2671111, -110.8507778, .753)
    #    elif OBSname == "VLT":
    #       #VLT location: Note make sure the coordinates are for the telescope to be used
    #       obsName = 'VLT'
    #       (obs_lat, obs_lon, obs_altitude) = (-24.6275, -70.4044, 2.650)
    #    elif OBSname == "VISTA":
    #       #VISTA Telescope location:
    #       obsName = 'VISTA'
    #       (obs_lat, obs_lon, obs_altitude) = (-24.6157000, -70.3976000, 2.635)
    #    elif OBSname == "CHILESCOPE":
    #       #CHILESCOPE Ritchey-Cretain 1m Telescope location:
    #       obsName = 'CHILESCOPE'
    #       (obs_lat, obs_lon, obs_altitude) = (-30.4708333333333,
    #           -70.7647222222222, 1.580)
    #    elif OBSname == "IAC80":
    #       #El Teide Observatory, IAC80 telescope:
    #       obsName = 'IAC80'
    #       (obs_lat, obs_lon, obs_altitude) = (+28.29966667, -16.51102778,
    #           2.38125)
    #    elif OBSname == "CA":
    #       #Calar Alto  Observatory location
    #       obsName = 'CA'
    #       (obs_lat, obs_lon, obs_altitude) = (37.22364444, -2.54621667, 2.168)
    #    else:
    #       print("OBSname = %s  not found...\n" % (OBSname))
################################################################################
################################################################################
################################################################################
