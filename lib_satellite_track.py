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

# Store orbital computations in file
#print the columns header of sat data to be displayed
# Note the angular speed of the satellite is in the AZ,EL (or AZ,ALT) frame
## Convert using str.join and a function like list_to_str
ut_time = 'UT Date, UT time'
lla_sat = 'Sat(lon) [deg], Sat(lat) [deg], Sat(alt) [km]'
angular_sat = 'Sat(Azimuth) [deg], Sat(Elevation), [deg] SatRA[hr], SatDEC[deg]'
angular_sun = 'SunRA[hr], SunDEC[deg], SunZenithAngle[deg]'
speed_sat = 'SatAngularSpeed [arcsecs/sec]'

colum_headers = f'{ut_time}, {lla_sat}, {angular_sat}, {angular_sun}, {speed_sat}'

################################################################################
# str manipulation

def data_formating_to_file(date_obj, darksat_latlon, sat_az, sat_alt,
    raSAT_h, raSAT_m, raSAT_s, decSAT_d, decSAT_m, decSAT_s,
    sunRA, sunDEC, sun_zenith_angle, ang_motion):

    computed_data_str = [
        f'{date_obj}\t', f'{darksat_latlon[0]:9.6f}\t',
        f'{darksat_latlon[1]:9.6f}\t', f'{darksat_latlon[2]:5.2f}\t',
        f'{sat_az:06.3f}\t',
        f'{sat_alt:06.3f} ',
        f'{raSAT_h:02d}h{raSAT_m:02d}m{raSAT_s:05.3f}s ',
        f'{decSAT_d:03d}:{decSAT_m:02d}:{decSAT_s:05.3f} ',
        f'{sunRA:09.7f} ', f'{sunDEC:09.7f} ',
        f'{sun_zenith_angle:07.3f} ', f'{ang_motion:08.3f}'
    ]

    data_str_to_file = ''.join(computed_data_str)

    return data_str_to_file

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

        print(f'Observatory: {obs_name}')
        print(f'Observatory latitude: {obs_lat}')
        print(f'Observatory latitude: {obs_lon}')
        print(f'Observatory latitude: {obs_altitude}')
        print(f'Satellite ID: {satellite_ID}')
        print(f'Forecast date: {day}/{month}/{year}\n')

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

    return dd*dec_sign, mm, ss
################################################################################
