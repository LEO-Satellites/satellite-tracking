import math
import os
import sys
import urllib

from datetime import datetime
import ephem
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital

from lib_satellite_track import input_handler
from lib_satellite_track import radians_to_deg, radians_to_hrs
from lib_satellite_track import radians_to_hh_mm_ss, dec_to_dd_mm_ss

################################################################################

(obs_name, obs_lat, obs_lon, obs_altitude,
    year, month, day,
    satellite_ID, satellite_brand) = input_handler(arguments=sys.argv)

print(f'Observatory: {obs_name}')
print(f'Observatory latitude: {obs_lat}')
print(f'Observatory latitude: {obs_lon}')
print(f'Observatory latitude: {obs_altitude}')
print(f'Satellite ID: {satellite_ID}')
print(f'Forecast date: {day}/{month}/{year}\n')

################################################################################

observer = ephem.Observer()
observer.epoch = '2000'
observer.pressure= 1010
observer.temp = 15
observer.lon = np.radians(obs_lon)
observer.lat = np.radians(obs_lat)
observer.elevation = obs_altitude*1000

sat_tle_url =\
    f'https://celestrak.com/NORAD/elements/supplemental/{satellite_brand}.txt'
tle_file = f'tle_{satellite_brand}.txt'

if not os.path.exists(tle_file):
    # pending to rise exeption if not able to retrieve file
    flag = urllib.request.urlretrieve(sat_tle_url, tle_file)

darksat = Orbital(satellite_ID, tle_file=f'./{tle_file}')
# print(darksat)

sat_az0 =0
sat_alt0 =0
hr0 = 0

#print the columns header of sat data to be displayed
# Note the angular speed of the satellite is in the AZ,EL (or AZ,ALT) frame
ut_time = 'UT Date, UT time'
lla_sat = 'Sat(lon) [deg], Sat(lat) [deg], Sat(alt) [km]'
angular_sat = 'Sat(Azimuth) [deg], Sat(Elevation), [deg] SatRA[hr], SatDEC[deg]'
angular_sun = 'SunRA[hr], SunDEC[deg], SunZenithAngle[deg]'
speed_sat = 'SatAngularSpeed [arcsecs/sec]'
strdata = f'{ut_time}, {lla_sat}, {angular_sat}, {angular_sun}, {speed_sat}'
print(strdata)
################################################################################
for hr in range(0, 24):

   for mn in range(0, 60):

       for secs in range(30, 31):

        # creates a date object
        date_obj = datetime(year, month, day, hr, mn, secs)

        # computes the current latitude, longitude of the satellite's footprint
        # and its current orbital altitude
        darksat_latlon = darksat.get_lonlatalt(date_obj)

        # uses the observer coordinates to compute the satellite azimuth and
        # elevation, negative elevation implies satellite is under the horizon
        sat_az, sat_alt = darksat.get_observer_look(
            date_obj, obs_lon, obs_lat, obs_altitude
            )

        # gets the Sun's RA and DEC at the time of observation
        sun_ra, sun_dec = pyorbital.astronomy.sun_ra_dec(date_obj)

        sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(
            date_obj, obs_lon, obs_lat
            )

        sunRA = radians_to_hrs(radians=sun_ra)
        sunDEC = radians_to_deg(radians=sun_dec)

        datestr ="%04d/%02d/%02d %02d:%02d:%02d" % (
            year, month, day, hr, mn, secs
            )

        observer.date = ephem.date(date_obj)


        ra, dec = observer.radec_of(np.radians(sat_az), np.radians(sat_alt))
###############################################################################
        # converts the RA to hh:mm:ss.sss
        raSAT = radians_to_deg(radians=ra)
        raSAT_h, raSAT_m, raSAT_s = radians_to_hh_mm_ss(ra)
###############################################################################
        # converts the DEC to dd:mm:ss
        decSAT = radians_to_deg(radians=dec)
        decSAT_d, decSAT_m, decSAT_s = dec_to_dd_mm_ss(dec=dec)
###############################################################################
        # print(sat_alt > 0 and sun_zenith_angle > 95 and sun_zenith_angle < 115)
        if sat_alt > 0 and sun_zenith_angle > 95 and sun_zenith_angle < 115:
           # compute the change in AZ and ALT of the satellite position between
           # this and previous observation

           # difference in azimuth between current and previous postions in
           # arcsecs
           daz  = (sat_az - sat_az0)*3600

           # difference in altitude between current and previous postions in arcsecs
           dalt = (sat_alt - sat_alt0)*3600

           # difference in time stamps between current and previous observation
           # in seconds of time
           dt = ((hr + mn/60. + secs/3600.) - hr0)*3600.

           # sets the current sat position and time, as the "previous" for next
           # observation
           sat_az0 = sat_az
           sat_alt0 = sat_alt
           hr0 = hr + mn/60. + secs/3600.

           ang_motion = math.sqrt(math.pow(daz,2) + math.pow(dalt,2))/dt

           # prints out the UT time, and satellite footprint position as well as
           # satellite azimuth and elevation at the observer location
           strdata = "%s\t%9.6f\t%9.6f\t%5.2f\t%06.3f\t%06.3f %02dh%02dm%05.3fs %03d:%02d:%05.3f %09.7f %09.7f %07.3f %08.3f" % (date_obj, darksat_latlon[0], darksat_latlon[1], darksat_latlon[2], sat_az, sat_alt, raSAT_h, raSAT_m, raSAT_s, decSAT_d, decSAT_m, decSAT_s, sunRA, sunDEC, sun_zenith_angle, ang_motion)
           print(strdata)

        else:
          # keeps copy of the current AZ, ALT and time information to derive
          # angular speed of the satellite in the AZ,EL frame
          sat_az0 = sat_az
          sat_alt0 = sat_alt
          hr0 = hr + mn/60. + secs/3600.
