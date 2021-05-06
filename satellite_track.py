#! /usr/bin/env python3.8
from argparse import ArgumentParser
import math
import os
import sys
import time
import urllib

from datetime import datetime, timezone
import ephem
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital

from lib_satellite_track import colum_headers
from lib_satellite_track import data_formating, time_stamp
from lib_satellite_track import observatory_pro

from lib_satellite_track import radians_to_deg
from lib_satellite_track import dec_to_dd_mm_ss
from lib_satellite_track import ra_to_hours, ra_to_hh_mm_ss

from constants_satellite_track import observatories
from lib_satellite_track import download_tle
###############################################################################
ti = time.time()
################################################################################
parser = ArgumentParser()
############################################################################
parser.add_argument('--year', '-y', type=int)
parser.add_argument('--month','-m', type=int)
parser.add_argument('--day', '-d', type=int)
############################################################################
# parser.add_argument('--satellite_ID', '-s_ID', type=str)
parser.add_argument('--satellite_brand', '-sb', type=str)
# parser.add_argument('--output_file', '-o', type=str)
parser.add_argument('--observatory', '-obs', type=str)
############################################################################
script_arguments = parser.parse_args()
################################################################################
year = script_arguments.year
month = script_arguments.month
day = script_arguments.day
############################################################################
satellite_brand = script_arguments.satellite_brand
# output_file = script_arguments.output_file
observatory = script_arguments.observatory

working_dir = f'/home/edgar/Documents/satellite-tracking'
################################################################################
output_dir = f'{working_dir}/output'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_fname = f'{observatory}_{satellite_brand}_{time_stamp()}'
##############################################################
with open(f'{output_dir}/{output_fname}.txt', 'a') as file:
    file.write(f'{colum_headers}\n')

with open(f'{output_dir}/{output_fname}_simple.txt', 'a') as file_simple:
    file_simple.write(f'date\ttime\tra\tdec\n')
################################################################################
tle_dir = f'/home/edgar/Documents/satellite-tracking/tle_dir'
tle_file = download_tle(satellite_brand, tle_dir)
# tle_file = 'tle_oneweb.txt' # Angel
satellites_list = []

with open(f'{tle_dir}/{tle_file}', 'r') as tle:

    lines_tle = tle.readlines()

    for idx, l in enumerate(lines_tle):

        if idx%3==0:
            satellites_list.append(l.strip())
################################################################################
observer = ephem.Observer()
observer.epoch = '2000'
observer.pressure= 1010
observer.temp = 15
########################################################################
observatories = observatory_pro(observatories)

data = observatories[observatory]

obs_lat = data['latitude']
obs_lon = data['longitude']
obs_altitude = data['altitude']/1000. # in km
################################################################################
observer.lon = np.radians(obs_lon)
observer.lat = np.radians(obs_lat)
observer.elevation = data['altitude']# in meters
############################################################################
for satellite in satellites_list[58:59]:
    print(satellite)
    with open(f'{output_dir}/{output_fname}.txt', 'a') as file:
        file.write(f'{satellite}\n')

    with open(f'{output_dir}/{output_fname}_simple.txt', 'a') as file_simple:
        file_simple.write(f'{satellite}\n')

    darksat = Orbital(satellite, tle_file=f'{tle_dir}/{tle_file}')
    ############################################################################
    sat_az0 =0
    sat_alt0 =0
    hr0 = 0
    ############################################################################
    for hr in range(0, 24):
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
            if sat_alt > 35 and sun_zenith_angle > 95 and sun_zenith_angle < 125:
            #Angel
            # if sat_alt > 0 and sun_zenith_angle > 95 and sun_zenith_angle < 115:

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

                ang_motion = math.sqrt(math.pow(daz,2) + math.pow(dalt,2))/dt
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
                ################################################################
                with open(f'{output_dir}/{output_fname}.txt', 'a') as file:
                    file.write(f'{data_str}\n')

                with open(f'{output_dir}/{output_fname}_simple.txt', 'a') as file_simple:
                    file_simple.write(f'{data_str_simple}\n')
                ################################################################
            else:
                # keeps copy of the current AZ, ALT and time information
                # to derive angular speed of the satellite in the AZ,EL frame
                sat_az0 = sat_az
                sat_alt0 = sat_alt
                hr0 = hr + mn/60. + secs/3600.
################################################################################
tf = time.time()
print(f'Running time: {tf-ti:.2} [s]')
