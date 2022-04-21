# LEOsat tracking
Low Earth orbit Satellite tracking code using supplemental TLE data from
Celestrak to calculate times and positions of LEOsats to plan observations.

# How to use the package:

## Low resolution track

* Set observing parameters in configuration file: track.ini
* run via terminal with: python track.py

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
