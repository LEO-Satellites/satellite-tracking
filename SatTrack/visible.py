##############################################################################
# Satellite tracking code using TLE data from Celestrak to calculate times
# and positions of LEOsats to plan observations.
# Written by
# Edgar Ortiz edgar.ortiz@uamail.cl
# Jeremy Tregloan-Reed jeremy.tregloan-reed@uda.cl
################################################################################
import os
import random
import sys
import time
import urllib

####################################################################
# from datetime import datetime, timezone
import datetime
import ephem
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital

####################################################################
from SatTrack.format import format
from SatTrack.units import convert

################################################################################
def get_observatory_data(observatories: "dict"):
    # converts to format used by otarola

    satellite_track = {}
    ############################################################################
    for observatory, data in observatories.items():

        otarola_format = {}
        ########################################################################
        for key, val in data.items():

            if type(val) == type([]):
                signo = 1
                otarola_format[key] = 0
                ################################################################
                for idx, f in enumerate(val):

                    if f < 0:
                        signo = -1
                        f = abs(f)

                    otarola_format[key] += f / 60 ** idx
                ################################################################
                otarola_format[key] = signo * otarola_format[key]

            else:
                otarola_format[key] = val

            if key == "longitude":

                if otarola_format[key] > 180.0:
                    otarola_format[key] = 360 - otarola_format[key]

                else:
                    otarola_format[key] = -otarola_format[key]

        satellite_track[observatory] = otarola_format
        ########################################################################
    ############################################################################
    return satellite_track


################################################################################
def set_window(day: "int", window: "str", tz):
    # datetime_object?
    ############################################################################
    if window == "evening":

        hour = 12 + tz

        if hour >= 24:
            hour -= 24

        elif hour < 0:
            hour += 24

        return hour, day
    ############################################################################
    elif window == "morning":

        hour = 0 + tz

        if hour < 0:
            day -= 1

        if hour >= 24:
            hour -= 24

        elif hour < 0:
            hour += 24

        return hour, day
    ############################################################################
    else:
        print(f'window keyword must be of either "morning" or "evening"')
        sys.exit()


################################################################################
def compute_visible(
    satellite: "str",
    window: "str",
    observatory_data: "dict",
    tle_file: "str",
    year: "int",
    month: "int",
    day: "int",
    seconds_delta: "int",
    satellite_altitude_lower_bound: "float",
    sun_zenith_lower: "float",
    sun_zenith_upper: "float",
) -> "list":

    """
    Computes when a satellite is visible

    PARAMETERS

        satellite: satellite type, e.g, oneweb or starlink
        window: time frame for obsevation, e.g, evening
        observatory_data:
        tle_file: name of tle file to use for computations
        year: year of the observation
        month: month of the observation
        day: day of the observation
        seconds_delta: time step to update satellite's dynamics
        satellite_altitude_lower_bound:
        sun_zenith_lower:
        sun_zenith_upper:

    OUTPUT

    """
    ############################################################################
    observer = ephem.Observer()
    observer.epoch = "2000"
    observer.pressure = 1010
    observer.temp = 15
    ################################################################
    observatory_latitude = observatory_data["latitude"]
    observer.lat = np.radians(observatory_latitude)
    ################################################################
    observatory_longitude = observatory_data["longitude"]
    observer.lon = np.radians(observatory_longitude)
    ################################################################
    observatory_altitude = observatory_data["altitude"] / 1000.0  # in km
    observer.elevation = observatory_data["altitude"]  # in meters
    ################################################################
    observatory_time_zone = observatory_data["tz"]
    ############################################################################
    darksat = Orbital(satellite, tle_file=f"{tle_file}")
    ############################################################################
    hour, day = set_window(day=day, window=window, tz=observatory_time_zone)
    ############################################################################
    # if time_delta = 60, then it will move minute by minute
    time_delta = datetime.timedelta(seconds=seconds_delta)
    date_time = datetime.datetime(year, month, day, hour, minute=0, second=0)
    ############################################################################
    satellite_azimuth0 = 0
    satellite_altitude0 = 0
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
            darksat_latitude_logitude = darksat.get_lonlatalt(date_time)
        except:
            return None
        ####################################################################
        # uses the observer coordinates to compute the satellite azimuth
        # and elevation, negative elevation implies satellite is under
        # the horizon
        satellite_azimuth, satellite_altitude = darksat.get_observer_look(
            date_time,
            observatory_longitude,
            observatory_latitude,
            observatory_altitude,
        )
        ####################################################################
        # gets the Sun's RA and DEC at the time of observation
        sun_ra, sun_dec = pyorbital.astronomy.sun_ra_dec(date_time)

        sun_RA = convert.ra_to_hours(ra=sun_ra)
        sun_DEC = convert.radians_to_deg(radians=sun_dec)
        ####################################################################
        sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(
            date_time, observatory_longitude, observatory_latitude
        )
        ####################################################################
        observer.date = ephem.date(date_time)
        ra, dec = observer.radec_of(
            np.radians(satellite_azimuth), np.radians(satellite_altitude)
        )
        ####################################################################
        ra_satellite_h, ra_satellite_m, ra_satellite_s = convert.ra_to_hh_mm_ss(
            ra
        )
        dec_satellite_d, dec_satellite_m, dec_satellite_s = convert.dec_to_dd_mm_ss(
            dec=dec
        )
        ####################################################################
        visible = (satellite_altitude > satellite_altitude_lower_bound) and (
            sun_zenith_lower < sun_zenith_angle < sun_zenith_upper
        )

        if visible:
            ################################################################
            # compute the change in AZ and ALT of the satellite position
            # between current and previous observation
            ## difference in azimuth arcsecs
            delta_azimuth = (satellite_azimuth - satellite_azimuth0) * 3600
            ## difference in altitude in arcsecs
            delta_altitude = (satellite_altitude - satellite_altitude0) * 3600
            ####################################################################
            dt = time_delta.total_seconds()
            angular_velocity = (
                np.sqrt(delta_azimuth ** 2 + delta_altitude ** 2) / dt
            )

            data_str, data_str_simple = format.data_formating(
                date_time,
                darksat_latitude_logitude,
                satellite_azimuth,
                satellite_altitude,
                ra_satellite_h,
                ra_satellite_m,
                ra_satellite_s,
                dec_satellite_d,
                dec_satellite_m,
                dec_satellite_s,
                sun_RA,
                sun_DEC,
                sun_zenith_angle,
                angular_velocity,
            )
            ####################################################################
            write.append([data_str, data_str_simple])
        ########################################################################
        # current position, time as the "previous" for next observation
        satellite_azimuth0 = satellite_azimuth
        satellite_altitude0 = satellite_altitude
        date_time += time_delta
    ############################################################################
    if len(write) > 0:
        return [[satellite] + data for data in write]


################################################################################
