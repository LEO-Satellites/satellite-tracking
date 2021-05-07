#! /usr/bin/env python3
import os
import sys
import time
import urllib

import numpy as np

from lib_satellite_track import colum_headers
from lib_satellite_track import observatory_pro

from constants_satellite_track import observatories
from lib_satellite_track import download_tle, compute_visible, input_handler
###############################################################################
ti = time.time()
################################################################################
satellite_brand, observatory, year, month, day, window = input_handler(
    arguments=sys.argv)
################################################################################
working_dir = f'/home/edgar/Documents/satellite-tracking'
################################################################################
output_dir = f'{working_dir}/output_files'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_fname = (f'visible-leosats_{observatory}_'
    f'{year}_{month:02}_{day:02}_{window}')

output_fname_simple = (f'observing-details_{observatory}_'
    f'{year}_{month:02}_{day:02}_{window}')

##############################################################
with open(f'{output_dir}/{output_fname}.txt', 'w') as file:
    file.write(f'{colum_headers}\n')

with open(f'{output_dir}/{output_fname_simple}.txt', 'w') as file_simple:
    file_simple.write(f'Date(UT)\tTime(UT)\tRA(hh:mm:ss)\tDEC(dd:mm:ss)\n')
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
observatories = observatory_pro(observatories)

observatory_data = observatories[observatory]

for satellite in satellites_list:
    print(satellite)
    compute_visible(
        satellite,
        window,
        observatory_data,
        output_fname,
        output_fname_simple,
        tle_file,
        year, month, day,
        output_dir)
################################################################################
tf = time.time()
print(f'Running time: {tf-ti:.2} [s]')
