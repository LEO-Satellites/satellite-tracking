##############################################################################
# Satellite tracking code using TLE data from Celestrak to calculate times
# and positions of LEOsats to plan observations.
# Written by
# Edgar Ortiz edgar.ortiz@uamail.cl
# Jeremy Tregloan-Reed jeremy.tregloan-reed@uda.cl
##############################################################################
#! /usr/bin/env python3
from configparser import ConfigParser, ExtendedInterpolation
from functools import partial
import multiprocessing as mp
import os
import time
################################################################################
import numpy as np
import pandas as pd
################################################################################
from SatTrack.constants import column_headers, observatories
from SatTrack.visible import get_observatory_data, input_handler
from SatTrack.visible import compute_visible, download_tle
from SatTrack.output import output_format
################################################################################
if __name__ == '__main__':
    ############################################################################
    ti = time.time()
    ############################################################################
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read('visibility.ini')
    ############################################################################
    # writing results
    output_dir = parser.get('directories', 'output_dir')
    data_output_dir = parser.get('directories', 'data_output_dir')
    if not os.path.exists(data_output_dir):
        os.makedirs(data_output_dir)
    ############################################################################
    # downloading tle file
    ## update this block to use pandas DataFrame :)
    satellite_brand = parser.get('configuration', 'satellite_brand')

    tle_dir = parser.get('directories', 'tle_dir')
    tle_fname = download_tle(satellite_brand, tle_dir)
    tle_file_path = f'{tle_dir}/{tle_fname}'

    satellites_list = []

    with open(f'{tle_dir}/{tle_fname}', 'r') as tle:

        lines_tle = tle.readlines()

        for idx, l in enumerate(lines_tle):

            if idx%3==0:
                satellites_list.append(l.strip())
    ############################################################################
    observatories = get_observatory_data(observatories)
    satellite_brand = parser.get('configuration', 'satellite_brand')
    observatory = parser.get('configuration', 'observatory')
    observatory_data = observatories[observatory]
    ############################################################################
    day = parser.getint('configuration', 'day')
    month = parser.getint('configuration', 'month')
    year = parser.getint('configuration', 'year')

    window = parser.get('configuration', 'window')
    ############################################################################
    sat_alt_lower_bound = parser.getfloat('satellite observing limits',
                                        'sat_alt_lower_bound')

    ############################################################################
    sun_zenith_range = parser.get('satellite observing limits',
                                  'sun_zenith_angle_range')

    sun_zenith_lower, sun_zenith_upper = sun_zenith_range.split(',')

    (sun_zenith_lower, sun_zenith_upper) = (float(sun_zenith_lower),
                                            float(sun_zenith_upper))
    ############################################################################
    compute_visible_parallel = partial(compute_visible,
                                       window=window,
                                       observatory_data=observatory_data,
                                       tle_file=tle_file_path,
                                       year=year, month=month, day=day,
                                       sat_alt_lower_bound=sat_alt_lower_bound,
                                       sun_zenith_lower=sun_zenith_lower,
                                       sun_zenith_upper=sun_zenith_upper)

    with mp.Pool(processes=None) as pool:
        results = pool.map(compute_visible_parallel, satellites_list)
    ############################################################################
    # Prepare data for DataFrame
    columns_df = ['satellite']

    columns_df = columns_df + [header.strip()
        for header in column_headers.split(',')]
    # all columns nan except the satellite column
    orbital_library_crash = [np.nan for _ in columns_df[:-1]]
    ############################################################################
    data_crash_satellites = []
    data_simple_crash_satellites = []
    visible_satellites = []

    for satellite in results:

        if satellite == None:

            satellite_name = ['crash']
            data_crash_satellites.append(satellite_name + orbital_library_crash)
            data_simple_crash_satellites.append(
                satellite_name + orbital_library_crash[:4])
        else:

            visible_satellites.append(satellite)
    ############################################################################
    # Prepare visible satellites data frame
    data_visible_satellites = []
    data_simple_visible_satellites = []

    for visible in visible_satellites:

        for visible_ in visible:

            [satellite, data, data_simple] = visible_
            data_visible_satellites.append([satellite] + data)
            data_simple_visible_satellites.append([satellite] + data_simple)
    ############################################################################
    # create DataFrame all data
    data_df = data_visible_satellites + data_crash_satellites
    observations_df = pd.DataFrame(columns=columns_df, data=data_df)

    details_name = parser.get('names', 'complete_output')

    observations_df = output_format(data_frame=observations_df,
        file_name=details_name,
        simple=False,
        output_directory=data_output_dir)
    ############################################################################
    # create DataFrame simple data
    columns_df = ['satellite',
        'date[UT]', 'time[UT]', 'RA[hh:mm:ss]', 'DEC[hh:mm:ss]']

    data_df = data_simple_visible_satellites #+ data_simple_crash_satellites

    visible_df = pd.DataFrame(columns=columns_df, data=data_df)

    visible_name = parser.get('names', 'simple_output')

    observations_df = output_format(data_frame=visible_df,
        file_name=visible_name,
        simple=True,
        output_directory=data_output_dir)
# Modify output such I only use the df with all data :)
################################################################################
    tf = time.time()
    print(f'Running time: {tf-ti:.2} [s]')
