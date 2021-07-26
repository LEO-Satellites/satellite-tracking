##############################################################################
# Satellite tracking code using TLE data from Celestrak to calculate times 
# and positions of LEOsats to plan observations.
# Written by 
# Edgar Ortiz edgar.ortiz@uamail.cl 
# Jeremy Tregloan-Reed jeremy.tregloan-reed@uda.cl 
##############################################################################


#! /usr/bin/env python3
from functools import partial
import multiprocessing as mp
import os
import sys
import time
import urllib
import random

import numpy as np

from constants_satellite_track import colum_headers, observatories
from lib_satellite_track import get_observatory_data, input_handler
from lib_satellite_track import compute_visible, download_tle

if __name__ == '__main__':
###############################################################################
    ti = time.time()
################################################################################
    satellite_brand, observatory, year, month, day, window = input_handler(
        arguments=sys.argv)
################################################################################
    working_dir = f'./Output/'
################################################################################
    output_dir = f'{working_dir}/output_files'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_fname = (f'visible-{satellite_brand}s_{observatory}_'
                    f'{year}_{month:02}_{day:02}_{window}')

    output_fname_simple = (f'observing-details_for-{satellite_brand}_{observatory}_'
                           f'{year}_{month:02}_{day:02}_{window}')

##############################################################
    with open(f'{output_dir}/{output_fname}.txt', 'w') as file:
        file.write(f'{colum_headers}\n')

    with open(f'{output_dir}/{output_fname_simple}.txt', 'w') as file_simple:
        file_simple.write(f'Date(UT)\tTime(UT)\tRA(hh:mm:ss)\tDEC(dd:mm:ss)\n')
################################################################################
    tle_dir = f'./Output/tle_data/'
    tle_file = download_tle(satellite_brand, tle_dir)
    satellites_list = []

    with open(f'{tle_dir}/{tle_file}', 'r') as tle:

        lines_tle = tle.readlines()

        for idx, l in enumerate(lines_tle):

            if idx%3==0:
                satellites_list.append(l.strip())
################################################################################
    observatories = get_observatory_data(observatories)

    observatory_data = observatories[observatory]

    compute_visible_parallel = partial(compute_visible,
                                       window=window,
                                       observatory_data=observatory_data,
                                       output_fname=output_fname,
                                       output_fname_simple=output_fname_simple,
                                       tle_file=tle_file,
                                       year=year, month=month, day=day,
                                       output_dir=output_dir)

    with mp.Pool(processes=None) as pool:
        res = pool.map(compute_visible_parallel, satellites_list)
################################################################################
    visible_satellites = []

    for satellite in res:

        if satellite == None:
            continue

        visible_satellites.append(satellite)
################################################################################
    observing_time = np.empty(len(visible_satellites))

    for idx, visible in enumerate(visible_satellites):

        [satellite, data_str, data_str_simple] = visible

        obs_time = data_str_simple.split('\t')[1].split(':')

        hours = float(obs_time[0])
        if hours < 3:
            hours += 24

        minutes = float(obs_time[1])/60.
        seconds = float(obs_time[2][:-1])/3600.

        obs_time = hours + minutes + seconds

        observing_time[idx] = obs_time
################################################################################

    obs_time_sort_ids = np.argsort(observing_time)

    for sort_id in obs_time_sort_ids:

        [satellite, data_str, data_str_simple] = visible_satellites[sort_id]

        with open(f'{output_dir}/{output_fname}.txt',
                  'a') as file:
            file.write(f'{satellite}\n{data_str}\n')

        with open(f'{output_dir}/{output_fname_simple}.txt',
                  'a') as file_simple:
            file_simple.write(f'{satellite}\n{data_str_simple}\n')
################################################################################
    tf = time.time()
    print(f'Running time: {tf-ti:.2} [s]')
