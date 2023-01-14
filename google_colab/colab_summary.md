# General overview: running track.py in the cloud with **Google-Colab** 

* The code enables parallel processing in the **Google-Colab** environment, allowing it to utilize multiple cores to speed up computations.
* It clones the **[satellite-tracking repository](https://github.com/CLEOsat-group/satellite-tracking)** from GitHub and installs the required dependencies listed in the **requirements.txt** file.
* Then it reads the contents of the **track.ini** configuration file and parses it using the ``configparser`` library.
* Afterwards it updates the values of various sections in the **track.ini** file, including the time, observation, TLE, directory, file, and configuration sections.
* It writes the modified configuration back to the **track.ini** file.
* Then runs the **track.py** script to perform the satellite tracking.
* Finally, it creates a zip archive of the output which in **Google-Colab** is located in the `/content/satellite-tracking/output/` directory and downloads it to the user's computer.

# Wall time in free Google-Colab

All the experiments were run with this configuration file for track.py
| **Satellite** 	| **Wall time [s]** 	|
|---	|:---:	|
| oneweb 	| 267.01 	|
| starlink 	| 1703.89 	|

```python
# [time] section
config['time']['year'] = '2023'
config['time']['month'] = '1'
config['time']['day'] = '15'
config['time']['delta'] = '60'
config['time']['window'] = 'morning'

# [observation] section
config['observation']['observatory'] = "lasilla"
config['observation']['satellite'] = "oneweb"
config['observation']['lowest_altitude_satellite'] = '30'
config['observation']['sun_zenith_lowest'] = '100'
config['observation']['sun_zenith_highest'] = '111'

# [tle] section
config['tle']['download'] = 'True'
# if download = False, load file below
config['tle']['name'] = 'tle_starlink_2022-10-11_13_12_01.txt'

# [directory] section
# DO NOT MODIFY THIS SECTION
config['directory']['work'] = os.getcwd()
config['directory']['output'] = f"{config['directory']['work']}/output"

# [file] section
config['file']['simple'] = 'observing-details'
config['file']['complete'] = 'visible'

# [configuration] section
config['configuration']['processes'] = '12'

```