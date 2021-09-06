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

# from datetime import datetime, timezone
import datetime
import ephem
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital
################################################################################
from SatTrack.format import format
from SatTrack.units import convert
################################################################################
################################################################################
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
def compute_visible(
    satellite:'str',
    window:'str',
    observatory_data:'dict',
    tle_file:'str',
    year,month,day,
    sat_alt_lower_bound,
    sun_zenith_lower,
    sun_zenith_upper
    ):


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
    hour0 = 0
    ############################################################################
    # datetime_object?
    if window=='evening':
        hours = [hour for hour in range(12, 24)]
        hours = [hour + obs_tz for hour in hours]
        hours = [hour-24 if hour>=24 else hour for hour in hours]
        hours = [hour+24 if hour<0 else hour for hour in hours]
    elif window=='morning':
        hours = [hour for hour in range(0, 13)]
        hours = [hour + obs_tz for hour in hours]
        if hours[0] < 0:
            day -= 1
        hours = [hour-24 if hour>=24 else hour for hour in hours]
        hours = [hour+24 if hour<0 else hour for hour in hours]
    else:
        print(f'window keyword must be of either "morning" or "evening"')
        sys.exit()
    ############################################################################
    write = []
    ############################################################################
    # date_time = datetime.datetime(
    #
    #     )
    # time_delta = datetime.timedelta(
    #
    # )
    for hour in hours:
        # Check logic with jeremy
        if  hours[0] != 0 and hour == 0:
            day += 1

        for minute in range(0, 60):

            for second in range(30, 31):

                date_obj = datetime.datetime(year, month, day, hour, minute, second)
                # computes the current latitude, longitude of the satellite's
                #footprint and its current orbital altitude
                try:
                    darksat_latlon = darksat.get_lonlatalt(date_obj)
                except:
                    # return [satellite, 'pyorbital crash', 'pyorbital crash']
                    return None
                    # This is for the data frame
                # uses the observer coordinates to compute the satellite azimuth
                # and elevation, negative elevation implies satellite is under
                # the horizon
                sat_az, sat_alt = darksat.get_observer_look(date_obj,
                    obs_lon, obs_lat, obs_altitude)
                # gets the Sun's RA and DEC at the time of observation
                sun_ra, sun_dec = pyorbital.astronomy.sun_ra_dec(date_obj)

                sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(
                    date_obj, obs_lon, obs_lat)

                sunRA = convert.ra_to_hours(ra=sun_ra)
                sunDEC = convert.radians_to_deg(radians=sun_dec)

                observer.date = ephem.date(date_obj)
                ra, dec = observer.radec_of(np.radians(sat_az), np.radians(sat_alt))
                ####################################################################
                # converts the RA to hh:mm:ss.sss
                raSAT_h, raSAT_m, raSAT_s = convert.ra_to_hh_mm_ss(ra)
                ####################################################################
                # converts the DEC to dd:mm:ss
                decSAT_d, decSAT_m, decSAT_s = convert.dec_to_dd_mm_ss(dec=dec)
                ####################################################################
                if (sat_alt > sat_alt_lower_bound and
                    (sun_zenith_lower < sun_zenith_angle < sun_zenith_upper)):
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
                    dt = ((hour + minute/60. + second/3600.) - hour0)*3600.
                    # sets the current sat position and time, as the "previous" for
                    # next observation
                    sat_az0 = sat_az
                    sat_alt0 = sat_alt
                    hour0 = hour + minute/60. + second/3600.

                    ang_motion = np.sqrt(np.power(daz,2) + np.power(dalt,2))/dt
                    # prints out the UT time, and satellite footprint position as well as
                    # satellite azimuth and elevation at the observer location
                    data_str, data_str_simple = format.data_formating(
                        date_obj,
                        darksat_latlon,
                        sat_az, sat_alt,
                        raSAT_h, raSAT_m, raSAT_s,
                        decSAT_d, decSAT_m, decSAT_s,
                        sunRA, sunDEC, sun_zenith_angle,
                        ang_motion)
                    ############################################################
                    write.append([data_str, data_str_simple])
                    ################################################################
                else:
                    # keeps copy of the current AZ, ALT and time information
                    # to derive angular speed of the satellite in the AZ,EL frame
                    sat_az0 = sat_az
                    sat_alt0 = sat_alt
                    hour0 = hour + minute/60. + second/3600.
                    ################################################################
    if len(write) > 0:

        # Return all the times for a satellite
        # [data_str, data_str_simple] = random.choice(write)
        # print(f'{satellite} is visible')
        # return [satellite, data_str, data_str_simple]
        # print(write)
        return [[satellite] + data for data in write]
        # return write
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
