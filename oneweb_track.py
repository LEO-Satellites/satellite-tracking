
#python code track_sat_revXXX.py

#revision 0.7
#date: January 15th, 2020
#updated: March 4th, 2020    calculation of RA and DEC for the Satellite and Sun was added
#updated: March 13th, 2020   calculation of satellite instantaenous angular motion (in AZ, EL frame) was added 
#updated: August 29, 2020    added coordinates for Chilescope and El Teide's IAC80 telescopes 
 
#Code by: Angel Otarola, aotarola@tmt.org

# Important information:
# run using python 3.7+ 
# needs installation of pyorbital, do: sudo pip install pyorbital
# needs installation of urllib, do: sudo pip install urllib3
# needs matplotlib, numpy, datetime (these are more standard python modules)


from pyorbital.orbital import Orbital
import pyorbital
from datetime import datetime
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import sys
import ephem
import math


nargs = len(sys.argv)

if nargs < 6:
#   print("Use: python track_sat.py OBSname SATid Year Month Day\nEx:  python track_sat_rev0p7.py IAC80 "STARLINK-1436 (VISORSAT)" 2020 8 31\n") 
   print("Use: python track_sat.py OBSname SATid Year Month Day\nEx:  python track_sat_rev0p7.py IAC80 \"STARLINK-1436 (VISORSAT)\" 2020 8 31\n") 
else:
   OBSname = sys.argv[1]
   if OBSname == "KPEAK":
      #Kitt Peak Observatory location
      obsName = 'K.P. Observatory'
      (obs_lat, obs_lon, obs_altitude) = (+31.9599, -111.5997, 2.067) 
   elif OBSname == "CTIO":
      #CTIO  Observatory location
      obsName = 'CTIO'
      (obs_lat, obs_lon, obs_altitude) = (-30.1690, -70.8063, 2.2)
   elif OBSname == "CKOIRAMA":
      #Ckoirama Observatory location
      obsName = 'Ckoirama Observatory'
      (obs_lat, obs_lon, obs_altitude) = (-24.08913333, -69.93058889, 0.966)
   elif OBSname == "HOME":
      #home location
      obsName = 'Home'
      (obs_lat, obs_lon, obs_altitude) = (+32.2671111, -110.8507778, .753)
   elif OBSname == "VLT":
      #VLT location: Note make sure the coordinates are for the telescope to be used
      obsName = 'VLT'
      (obs_lat, obs_lon, obs_altitude) = (-24.6275, -70.4044, 2.650)
   elif OBSname == "VISTA":
      #VISTA Telescope location:
      obsName = 'VISTA'
      (obs_lat, obs_lon, obs_altitude) = (-24.6157000, -70.3976000, 2.635)
   elif OBSname == "CHILESCOPE":
      #CHILESCOPE Ritchey-Cretain 1m Telescope location:
      obsName = 'CHILESCOPE'
      (obs_lat, obs_lon, obs_altitude) = (-30.4708333333333, -70.7647222222222, 1.580)
   elif OBSname == "IAC80":
      #El Teide Observatory, IAC80 telescope:
      obsName = 'IAC80'
      (obs_lat, obs_lon, obs_altitude) = (+28.29966667, -16.51102778, 2.38125)
   elif OBSname == "CA":
      #Calar Alto  Observatory location
      obsName = 'CA'
      (obs_lat, obs_lon, obs_altitude) = (37.22364444, -2.54621667, 2.168)
   else:
      print("OBSname = %s  not found...\n" % (OBSname))


   observer = ephem.Observer()
   observer.epoch = '2000'
   #observer.pressure = 760
   #observer.pressure = 906 
   observer.pressure= 1010
   observer.temp = 15 
   observer.lon = np.radians(obs_lon)
   observer.lat = np.radians(obs_lat)
   observer.elevation = obs_altitude*1000


   #Starlink Satellites TLE data /URL of the TLE data
   #sat_tle_url = "https://celestrak.com/NORAD/elements/supplemental/starlink.txt"
   
   #OneWeb satellites:
   sat_tle_ulr = "https://celestrak.com/NORAD/elements/supplemental/oneweb.txt"


   #retrieves the Starlinks TLE data from the web-site (a working internet link is needed)
   #out_fn = 'tle_darksat.txt'
   out_fn = 'tle_oneweb.txt'
   flag=urllib.request.urlretrieve(sat_tle_url, out_fn)

   satID = sys.argv[2]
   #satID = 'STARLINK-1130 (DARKSAT)'
   #satID = 'STARLINK-54'
   #darksat = Orbital(satID, tle_file='./tle_darksat.txt')
   darksat = Orbital(satID, tle_file='./tle_oneweb.txt')

   print(darksat)

   year  = int(sys.argv[3]) 
   month = int(sys.argv[4]) 
   day   = int(sys.argv[5])


   sat_az0 =0
   sat_alt0 =0
   hr0 = 0

   #print the columns header of sat data to be displayed
   # Note the angular speed of the satellite is in the AZ,EL (or AZ,ALT) frame
   strdata = "UT Date, UT time, Sat(lon) [deg], Sat(lat) [deg], Sat(alt) [km], Sat(Azimuth) [deg], Sat(Elevation) [deg] SatRA[hr] SatDEC[deg] SunRA[hr] SunDEC[deg] SunZenithAngle[deg] SatAngularSpeed [arcsecs/sec]" 
   print(strdata)

   for hr in range(0, 24):
       for mn in range(0, 60):
           for secs in range(30, 31):
   #        for secs in range(0, 60):
   #for hr in range(0, 1):
   #    for mn in range(0, 30):
   #        for secs in range(0, 60):
 
            # creates a date object
            dtobj = datetime(year, month, day, hr, mn, secs)
       
            # computes the current latitude, longitude of the satellite's footprint and its current orbital altitude
            darksat_latlon = darksat.get_lonlatalt(dtobj)

            # uses the observer coordinates to compute the satellite azimuth and elevation, negative elevation implies satellite is under the horizon
            sat_az, sat_alt = darksat.get_observer_look(dtobj, obs_lon, obs_lat, obs_altitude)


            # gets the Sun's RA and DEC at the time of observation
            sun_ra, sun_dec = pyorbital.astronomy.sun_ra_dec(dtobj) 
            sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(dtobj, obs_lon, obs_lat)

            sunRA = sun_ra*180./math.pi	# from radians to degrees
            if sunRA < 0:
               sunRA = 360+sunRA

            sunRA = sunRA*24./360   # from degrees to hours

            sunDEC = sun_dec*180./math.pi #changes from radians to degrees

            datestr ="%04d/%02d/%02d %02d:%02d:%02d" % (year, month, day, hr, mn, secs)
            #observer.date = ephem.date(datestr)
            observer.date = ephem.date(dtobj)

 
            #tm_tuple = (year, month, day, hr, mn, secs)
            #J0 = ephem.julian_date(0)
            #JD = ephem.julian_date(tm_tuple)
            #observer.date = JD-J0                     # these 4 lines of code produce same results
                                                       # than the two lines above it

            ra, dec = observer.radec_of(np.radians(sat_az), np.radians(sat_alt))
            raSAT = ra*180./math.pi
            if raSAT < 0:
               raSAT = 360+raSAT

            # converts the RA to hh:mm:ss.sss
            raSAT = raSAT*24./360
            raSAT_h=int(raSAT)
            raSAT_m=int((raSAT-raSAT_h)*60.)
            raSAT_s=(raSAT - (raSAT_h+raSAT_m/60.))*3600.

            decSAT = dec*180./math.pi

            # converts the DEC to dd:mm:ss
            if decSAT < 0:
               dec_sign = -1
               decSAT = abs(decSAT) 
            else:
               dec_sign = 1

            decSAT_d=int(decSAT)
            decSAT_m=int((decSAT-decSAT_d)*60.)
            decSAT_s=(decSAT - (decSAT_d+decSAT_m/60.))*3600.
            decSAT_d = dec_sign*decSAT_d
            decSAT = dec_sign*decSAT

            #if sat_alt > 0:
            if sat_alt > 0 and sun_zenith_angle > 90 and sun_zenith_angle < 120:
            #if sat_alt > -180:
               # compute the change in AZ and ALT of the satellite position between this and previous observation
               daz  = (sat_az - sat_az0)*3600			# difference in azimuth between current and previous postions in arcsecs
               dalt = (sat_alt - sat_alt0)*3600                 # difference in altitude between current and previous postions in arcsecs
               dt   = ((hr + mn/60. + secs/3600.) - hr0)*3600.  # difference in time stamps between current and previous observation in seconds of time

               # sets the current sat position and time, as the "previous" for next observation
               sat_az0 = sat_az
               sat_alt0 = sat_alt
               hr0 = hr + mn/60. + secs/3600.;

               ang_motion = math.sqrt(math.pow(daz,2) + math.pow(dalt,2))/dt

               # prints out the UT time, and satellite footprint position as well as satellite azimuth and elevation at the observer location
               strdata = "%s\t%9.6f\t%9.6f\t%5.2f\t%06.3f\t%06.3f %02dh%02dm%05.3fs %03d:%02d:%05.3f %09.7f %09.7f %07.3f %08.3f" % (dtobj, darksat_latlon[0], darksat_latlon[1], darksat_latlon[2], sat_az, sat_alt, raSAT_h, raSAT_m, raSAT_s, decSAT_d, decSAT_m, decSAT_s, sunRA, sunDEC, sun_zenith_angle, ang_motion)
               print(strdata)

            else:
              # keeps copy of the current AZ, ALT and time information to derive angular speed of the satellite in the AZ,EL frame
              sat_az0 = sat_az
              sat_alt0 = sat_alt
              hr0 = hr + mn/60. + secs/3600.; 

