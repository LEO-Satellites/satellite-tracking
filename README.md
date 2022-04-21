# Satellite-tracking
Low Earth orbit Satellite tracking code using supplemental TLE data from
Celestrak to calculate times and positions of LEOsats to plan observations.
After setting the observing parameters in the configuration file "track.ini"
the code can be run via terminal with the command: "python track.py"

This package uses:
* Pyorbital package (https://github.com/pytroll/pyorbital).
*
If this code is used in any published work, please cite the following
publications:
* Tregloan-Reed, J., et al. 2020, A&A, 637, L1
* Tregloan-Reed, J., et al. 2021, A&A, 647, A54

Written by:
* Edgar Ortiz, Universidad de Antofagasta: ed.ortizm@gmail.com
* Jeremy Tregloan-Reed, Univerisdad de Atacama: jeremy.tregloan-reed@uda.cl

The Original core code to determine satellite positional data from operator
released TLEs was written by Ángel Otarola.
