import math
import os
import sys
import urllib

from datetime import datetime, timezone
import ephem
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital

from lib_satellite_track import colum_headers
from lib_satellite_track import data_formating_to_file
from lib_satellite_track import input_handler
from lib_satellite_track import radians_to_deg, radians_to_hrs
from lib_satellite_track import radians_to_hh_mm_ss, dec_to_dd_mm_ss

################################################################################
# Handling script's external arguments
(obs_name, obs_lat, obs_lon, obs_altitude,
    year, month, day,
    satellite_ID, satellite_brand) = input_handler(arguments=sys.argv)
################################################################################
head_name = satellite_ID.replace('(', '_').replace(')', '_').replace(' ', '_')
output_fname = f'{head_name.lower()}_{year}_{month:02}_{day:02}.txt'
save_orbital_computations = open(f'{output_fname}', 'w')
save_orbital_computations.write(f'{colum_headers}\n')
################################################################################
observer = ephem.Observer()
observer.epoch = '2000'
observer.pressure= 1010
observer.temp = 15
observer.lon = np.radians(obs_lon)
observer.lat = np.radians(obs_lat)
observer.elevation = obs_altitude*1000
################################################################################
sat_tle_url =\
    f'https://celestrak.com/NORAD/elements/supplemental/{satellite_brand}.txt'

date_download = datetime.now(tz=timezone.utc)
year = date_download.year
month = date_download.month
day = date_download.day
hour = date_download.hour
minute = date_download.minute
second = date_download.second

time_stamp =\
    f'{year}-{month:02}-{day:02}-{hour:02}[h]:{minute:02}[m]:{second:02}[s]'

tle_file = f'tle_{satellite_brand}_{time_stamp}.txt'

flag = urllib.request.urlretrieve(sat_tle_url, tle_file)
#
# # if not os.path.exists(tle_file):
#
# #     flag = urllib.request.urlretrieve(sat_tle_url, tle_file)
# ################################################################################
# darksat = Orbital(satellite_ID, tle_file=f'./{tle_file}')
# # print(darksat)
# ################################################################################
# #??
# sat_az0 =0
# sat_alt0 =0
# hr0 = 0
# ################################################################################
# for hr in range(0, 24):
#
#    for mn in range(0, 60):
#
#        for secs in range(30, 31):
#
#         # creates a date object
#         date_obj = datetime(year, month, day, hr, mn, secs)
#
#         # computes the current latitude, longitude of the satellite's footprint
#         # and its current orbital altitude
#         darksat_latlon = darksat.get_lonlatalt(date_obj)
#
#         # uses the observer coordinates to compute the satellite azimuth and
#         # elevation, negative elevation implies satellite is under the horizon
#         sat_az, sat_alt = darksat.get_observer_look(
#             date_obj, obs_lon, obs_lat, obs_altitude
#             )
#
#         # gets the Sun's RA and DEC at the time of observation
#         sun_ra, sun_dec = pyorbital.astronomy.sun_ra_dec(date_obj)
#
#         sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(
#             date_obj, obs_lon, obs_lat
#             )
#
#         sunRA = radians_to_hrs(radians=sun_ra)
#         sunDEC = radians_to_deg(radians=sun_dec)
#
#         observer.date = ephem.date(date_obj)
#         ra, dec = observer.radec_of(np.radians(sat_az), np.radians(sat_alt))
# ###############################################################################
#         # converts the RA to hh:mm:ss.sss
#         raSAT = radians_to_deg(radians=ra)
#         raSAT_h, raSAT_m, raSAT_s = radians_to_hh_mm_ss(ra)
# ###############################################################################
#         # converts the DEC to dd:mm:ss
#         decSAT = radians_to_deg(radians=dec)
#         decSAT_d, decSAT_m, decSAT_s = dec_to_dd_mm_ss(dec=dec)
# ###############################################################################
#         if sat_alt > 30 and sun_zenith_angle > 95 and sun_zenith_angle < 125:
#            # compute the change in AZ and ALT of the satellite position between
#            # this and previous observation
#
#            # difference in azimuth between current and previous postions in
#            # arcsecs
#            daz  = (sat_az - sat_az0)*3600
#
#            # difference in altitude between current and previous postions in arcsecs
#            dalt = (sat_alt - sat_alt0)*3600
#
#            # difference in time stamps between current and previous observation
#            # in seconds of time
#            dt = ((hr + mn/60. + secs/3600.) - hr0)*3600.
#
#            # sets the current sat position and time, as the "previous" for next
#            # observation
#            sat_az0 = sat_az
#            sat_alt0 = sat_alt
#            hr0 = hr + mn/60. + secs/3600.
#
#            ang_motion = math.sqrt(math.pow(daz,2) + math.pow(dalt,2))/dt
#            # prints out the UT time, and satellite footprint position as well as
#            # satellite azimuth and elevation at the observer location
#            data_str_to_file = data_formating_to_file(date_obj, darksat_latlon,
#                sat_az, sat_alt, raSAT_h, raSAT_m, raSAT_s, decSAT_d, decSAT_m,
#                decSAT_s, sunRA, sunDEC, sun_zenith_angle, ang_motion
#            )
#
#            save_orbital_computations.write(f'{data_str_to_file}\n')
#
#         else:
#           # keeps copy of the current AZ, ALT and time information to derive
#           # angular speed of the satellite in the AZ,EL frame
#           sat_az0 = sat_az
#           sat_alt0 = sat_alt
#           hr0 = hr + mn/60. + secs/3600.
################################################################################
save_orbital_computations.close()
