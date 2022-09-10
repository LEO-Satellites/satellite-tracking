# LEOsat tracking
Low Earth orbit Satellite tracking code using supplemental TLE data from
Celestrak to calculate times and positions of LEOsats to plan observations.

# How to use the package:

## Low resolution track

* Set observing parameters in configuration file: track.ini
* run via terminal with: python track.py

### Sections in track.ini

[time]

    - year, month and day of observations
    - delta: time resolution for calculation in seconds
    - window: morning or evening


[observation]

    - observatory: available observatories are in observatories.py. Additional observatories can be appended to the file.
    - satellite: oneweb or starlink for instance

    Next items define visibility constraints:

    - lowest_altitude_satellite
    - sun_zenith_lowest
    - sun_zenith_highest

[tle]

    - download: if True to download and use the latest TLE file
    if False, load file below
    - name: tle_oneweb_2022-04-22-04:55:16.txt for instance

[directory]

    - work: location of repository in your machine
    - output: where to save data

[file]

    - simple: name of file with time stamp, RA and DEC of visible satellites
    - complete: name of file with detailed information of visible satellites

[configuration]

    - processes: number of cores to track satellites in parallel
## High resolution track with custom time window

* Set observing parameters in configuration file: custom_track.ini
* run via terminal with: python custom_track.py

This package relies on the following packages:
* pyorbital: https://github.com/pytroll/pyorbital.
* ephem: https://github.com/brandon-rhodes/pyephem
* Other packages listed in requirements.txt

If this code is used in any published work, please cite the following
publications:
* Tregloan-Reed, J., et al. 2020, A&A, 637, L1
* Tregloan-Reed, J., et al. 2021, A&A, 647, A54

Written by:
* Edgar Ortiz, Universidad de Antofagasta: ed.ortizm@gmail.com
* Jeremy Tregloan-Reed, Univerisdad de Atacama: jeremy.tregloan-reed@uda.cl

The Original core code to determine satellite positional data from operator
released TLEs was written by Ángel Otarola.
