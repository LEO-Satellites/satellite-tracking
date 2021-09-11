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
    year:'int',
    month:'int',
    day:'int',
    seconds_delta:'int',
    sat_alt_lower_bound:'float',
    sun_zenith_lower:'float',
    sun_zenith_upper:'float'
    )->'list':


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
        # e.g lasilla tz = 4
        hours = [hour for hour in range(12, 24)]
        # 12 - 23
        hours = [hour + obs_tz for hour in hours]
        # 16 - 27
        hours = [hour-24 if hour>=24 else hour for hour in hours]
        # 16 - 23 and 00 - 03
        hours = [hour+24 if hour<0 else hour for hour in hours]
        # ??
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
    # if time_delta = 60, then it will move minute by minute
    time_delta = datetime.timedelta(seconds=seconds_delta)

    date_obj = datetime.datetime(
        year, month, day,
        hour=hours[0],
        minute=0,
        second=0
        )
    ############################################################################
    write = []
    ############################################################################
    number_iterations = (12 * 60 * 60) / seconds_delta
    number_iterations = range(int(number_iterations))
    for time_step in number_iterations:
        ####################################################################
        # computes the current latitude, longitude of the satellite's
        # footprint and its current orbital altitude
        try:
            darksat_latlon = darksat.get_lonlatalt(date_obj)
        except:
            # return [satellite, 'pyorbital crash', 'pyorbital crash']
            return None
            # This is for the data frame
        ####################################################################
        # uses the observer coordinates to compute the satellite azimuth
        # and elevation, negative elevation implies satellite is under
        # the horizon
        sat_az, sat_alt = darksat.get_observer_look(
            date_obj,
            obs_lon,
            obs_lat,
            obs_altitude
            )
        ####################################################################
        # gets the Sun's RA and DEC at the time of observation
        sun_ra, sun_dec = pyorbital.astronomy.sun_ra_dec(date_obj)

        sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(
            date_obj,
            obs_lon,
            obs_lat
            )
        ####################################################################
        sunRA = convert.ra_to_hours(ra=sun_ra)
        sunDEC = convert.radians_to_deg(radians=sun_dec)
        ####################################################################
        observer.date = ephem.date(date_obj)
        ra, dec = observer.radec_of(
            np.radians(sat_az),
            np.radians(sat_alt)
            )
        ####################################################################
        # converts the RA to hh:mm:ss.sss
        raSAT_h, raSAT_m, raSAT_s = convert.ra_to_hh_mm_ss(ra)
        ####################################################################
        # converts the DEC to dd:mm:ss
        decSAT_d, decSAT_m, decSAT_s = convert.dec_to_dd_mm_ss(dec=dec)
        ####################################################################
        if (
            (sat_alt > sat_alt_lower_bound)
            and
            (sun_zenith_lower < sun_zenith_angle < sun_zenith_upper)
            ):
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
            # dt = ((hour + minute/60. + second/3600.) - hour0)*3600.
            dt = (
                (date_obj.hour + date_obj.minute/60. + date_obj.second/3600.)
                - hour0
                )*3600.
            # sets the current sat position and time, as the "previous" for
            # next observation
            sat_az0 = sat_az
            sat_alt0 = sat_alt
            hour0 = date_obj.hour + date_obj.minute/60. + date_obj.second/3600.
            ####################################################################
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
            ####################################################################
            write.append([data_str, data_str_simple])
        ########################################################################
        else:
            # keeps copy of the current AZ, ALT and time information
            # to derive angular speed of the satellite in the AZ,EL frame
            sat_az0 = sat_az
            sat_alt0 = sat_alt
            hour0 = date_obj.hour + date_obj.minute/60. + date_obj.second/3600.
        ########################################################################
        date_obj += time_delta
    ############################################################################
    if len(write) > 0:
        # Return all the times for a satellite
        # [data_str, data_str_simple] = random.choice(write)
        # print(f'{satellite} is visible')
        # return [satellite, data_str, data_str_simple]
        # print(write)
        return [[satellite] + data for data in write]
        # return write
################################################################################
