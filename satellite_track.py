import sys

import ephem

from lib_satellite_track import input_handler

################################################################################

(obs_name, obs_lat, obs_lon, obs_altitude,
    year, month, day, satellite_ID) = input_handler(arguments=sys.argv)

print(f'Observatory: {obs_name}')
print(f'Observatory latitude: {obs_lat}')
print(f'Observatory latitude: {obs_lon}')
print(f'Observatory latitude: {obs_altitude}')
print(f'Satellite ID: {satellite_ID}')
print(f'Forecast date: {day}/{month}/{year}')

################################################################################

observer = ephem.Observer()
observer.epoch = '2000'
observer.pressure= 1010
observer.temp = 15
observer.lon = np.radians(obs_lon)
observer.lat = np.radians(obs_lat)
observer.elevation = obs_altitude*1000
