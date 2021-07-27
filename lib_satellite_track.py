##############################################################################
# Satellite tracking code using TLE data from Celestrak to calculate times
# and positions of LEOsats to plan observations.
# Written by
# Edgar Ortiz edgar.ortiz@uamail.cl
# Jeremy Tregloan-Reed jeremy.tregloan-reed@uda.cl
##############################################################################
import os
import random
import sys
import time
import urllib

from datetime import datetime, timezone
import ephem
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital
################################################################################
def time_stamp():

    date = datetime.now(tz=timezone.utc)
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second

    stamp = (f'{year}_{month:02}_{day:02}_'
        f'{hour:02}h_{minute:02}m_{second:02}s')

    return stamp
################################################################################
def download_tle(satellite_brand:'str', tle_dir:'str'):

    sat_tle_url = (f'https://celestrak.com/NORAD/elements/supplemental/'
        f'{satellite_brand}.txt')

    tle_file = f'tle_{satellite_brand}_{time_stamp()}.txt'

    if not os.path.exists(tle_dir):
        os.makedirs(tle_dir)

    urllib.request.urlretrieve(sat_tle_url, f'{tle_dir}/{tle_file}')

    return tle_file
################################################################################
def get_observatory_data(observatories:'dict'):
    # converts to format used by otarola

    satellite_track = {}
    ############################################################################
    for observatory, data in observatories.items():

        otarola_format = {}
        ########################################################################
        for key, val in data.items():

            if type(val)==type([]):
                signo = 1
                otarola_format[key]=0
                ################################################################
                for idx, f in enumerate(val):

                    if f<0:
                        signo = -1
                        f = abs(f)

                    otarola_format[key] += f/60**idx
                ################################################################
                otarola_format[key] = signo*otarola_format[key]

            else:
                otarola_format[key]=val

            if key=='longitude':

                if otarola_format[key] > 180.:
                    otarola_format[key] = 360 - otarola_format[key]

                else:
                    otarola_format[key] = -otarola_format[key]

        satellite_track[observatory] = otarola_format
        ########################################################################
    ############################################################################
    return satellite_track
################################################################################
def data_formating(date_obj, darksat_latlon, sat_az, sat_alt,
    raSAT_h, raSAT_m, raSAT_s, decSAT_d, decSAT_m, decSAT_s,
    sunRA, sunDEC, sun_zenith_angle, ang_motion):

    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    hour = date_obj.hour
    minute = date_obj.minute
    second = date_obj.second

    date = f'{year}-{month:02}-{day:02}'
    time = f'{hour:02}:{minute:02}:{second:02}s'

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

    computed_data_str_simple = [
        f'{date}\t',
        f'{time}\t',
        f'{raSAT_h:02d}h{raSAT_m:02d}m{raSAT_s:05.3f}s\t',
        f'{decSAT_d:03d}:{decSAT_m:02d}:{decSAT_s:05.3f}'
        ]
    data_str = ''.join(computed_data_str)
    data_str_simple = ''.join(computed_data_str_simple)

    return data_str, data_str_simple
################################################################################
def ra_to_hours(ra):
    ra = ra*180./np.pi

    if ra < 0 :
        ra += 360

    ra = ra*(24./360.)

    return ra
################################################################################
def radians_to_deg(radians):

    deg = radians*180./np.pi

    return deg
################################################################################
def ra_to_hh_mm_ss(ra):
    # converts the RA to hh:mm:ss.sss

    hrs = ra_to_hours(ra)

    hh = int(hrs)

    mins = (hrs-hh)*60.
    mm = int(mins)

    ss = (mins-mm)*60

    return hh, mm, ss
################################################################################
def dec_to_dd_mm_ss(dec):
    # converts the DEC to dd:mm:ss
    dec = radians_to_deg(dec)

    if dec < 0:
       dec_sign = -1
       dec = abs(dec)
    else:
        dec_sign = 1

    dd = int(dec)

    mins = (dec-dd)*60.
    mm = int(mins)

    ss = (mins-mm)*60

    return dd*dec_sign, mm, ss
################################################################################
################################################################################
def compute_visible(satellite:'str', window:'str', observatory_data:'dict',
    output_fname:'str', output_fname_simple:'str', tle_file:'str',
    year, month, day):

    print(tle_file)

    observer = ephem.Observer()
    observer.epoch = '2000'
    observer.pressure= 1010
    observer.temp = 15
    ########################################################################
    obs_lat = observatory_data['latitude']
    obs_lon = observatory_data['longitude']
    obs_altitude = observatory_data['altitude']/1000. # in km
    obs_tz = observatory_data['tz']
    ################################################################################
    observer.lon = np.radians(obs_lon)
    observer.lat = np.radians(obs_lat)
    observer.elevation = observatory_data['altitude']# in meters
    ############################################################################
    flag = 0
    darksat = Orbital(satellite, tle_file=f'{tle_file}')
    ############################################################################
    sat_az0 =0
    sat_alt0 =0
    hr0 = 0
    ############################################################################
    if window=='evening':
        hours = [hr for hr in range(12, 24)]
        hours = [hr + obs_tz for hr in hours]
        hours = [hr-24 if hr>=24 else hr for hr in hours]
        hours = [hr+24 if hr<0 else hr for hr in hours]
    elif window=='morning':
        hours = [hr for hr in range(0, 13)]
        hours = [hr + obs_tz for hr in hours]
        if hours[0] < 0:
            day -= 1
        hours = [hr-24 if hr>=24 else hr for hr in hours]
        hours = [hr+24 if hr<0 else hr for hr in hours]
    else:
        print(f'window keyword must be of either "morning" or "evening"')
        sys.exit()
    ############################################################################
    write = []
    ############################################################################
    for hr in hours:
        if  hours[0] != 0 and hr == 0:
            day += 1

        for mn in range(0, 60):

            for secs in range(30, 31):

                date_obj = datetime(year, month, day, hr, mn, secs)

                # computes the current latitude, longitude of the satellite's
                #footprint and its current orbital altitude
                darksat_latlon = darksat.get_lonlatalt(date_obj)

                # uses the observer coordinates to compute the satellite azimuth
                # and elevation, negative elevation implies satellite is under
                # the horizon
                sat_az, sat_alt = darksat.get_observer_look(date_obj,
                    obs_lon, obs_lat, obs_altitude)

                # gets the Sun's RA and DEC at the time of observation
                sun_ra, sun_dec = pyorbital.astronomy.sun_ra_dec(date_obj)

                sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(
                    date_obj, obs_lon, obs_lat)

                sunRA = ra_to_hours(ra=sun_ra)
                sunDEC = radians_to_deg(radians=sun_dec)

                observer.date = ephem.date(date_obj)
                ra, dec = observer.radec_of(np.radians(sat_az), np.radians(sat_alt))
                ####################################################################
                # converts the RA to hh:mm:ss.sss
                raSAT_h, raSAT_m, raSAT_s = ra_to_hh_mm_ss(ra)
                ####################################################################
                # converts the DEC to dd:mm:ss
                # print(dec)
                decSAT_d, decSAT_m, decSAT_s = dec_to_dd_mm_ss(dec=dec)
                ####################################################################
                #us
                if sat_alt > 30 and sun_zenith_angle > 97 and sun_zenith_angle < 114:
                    ################################################################
                    # compute the change in AZ and ALT of the satellite position
                    # between this and previous observation
                    ################################################################
                    # difference in azimuth between current and previous postions in
                    # arcsecs
                    daz  = (sat_az - sat_az0)*3600

                    # difference in altitude between current and previous postions
                    # in arcsecs
                    dalt = (sat_alt - sat_alt0)*3600

                    # difference in time stamps between current and previous
                    # observation in seconds of time
                    dt = ((hr + mn/60. + secs/3600.) - hr0)*3600.

                    # sets the current sat position and time, as the "previous" for
                    # next observation
                    sat_az0 = sat_az
                    sat_alt0 = sat_alt
                    hr0 = hr + mn/60. + secs/3600.

                    ang_motion = np.sqrt(np.power(daz,2) + np.power(dalt,2))/dt
                    # prints out the UT time, and satellite footprint position as well as
                    # satellite azimuth and elevation at the observer location

                    data_str, data_str_simple = data_formating(
                        date_obj,
                        darksat_latlon,
                        sat_az, sat_alt,
                        raSAT_h, raSAT_m, raSAT_s,
                        decSAT_d, decSAT_m, decSAT_s,
                        sunRA, sunDEC, sun_zenith_angle,
                        ang_motion)
                    write.append([data_str, data_str_simple])
                    ################################################################
                else:
                    # keeps copy of the current AZ, ALT and time information
                    # to derive angular speed of the satellite in the AZ,EL frame
                    sat_az0 = sat_az
                    sat_alt0 = sat_alt
                    hr0 = hr + mn/60. + secs/3600.
                    ################################################################

    if len(write) > 0:

        [data_str, data_str_simple] = random.choice(write)
        print(f'{satellite} is visible')
        return [satellite, data_str, data_str_simple]
################################################################################
def input_handler(arguments):
    "arguments: list with arguments pass to the script"

    n_args = len(arguments)

    if n_args < 7 or n_args > 7:
        print(f'Use: python satellite_track.py sat_brand obs  Year Month Day window')
        print(f'Ex: python p_satellite_track.py oneweb eso 2021 05 07 morning')
        sys.exit()

    satellite_brand = arguments[1]
    observatory = arguments[2]

    year = int(arguments[3])
    month = int(arguments[4])
    day = int(arguments[5])

    window = arguments[6]
    ############################################################################
    return satellite_brand, observatory, year, month, day, window
###############################################################################
