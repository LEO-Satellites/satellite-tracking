#! /usr/bin/env python3
from configparser import ConfigParser, ExtendedInterpolation
from functools import partial
import multiprocessing as mp
import os
import sys
import time

################################################################################
import numpy as np
import pandas as pd

###############################################################################
from SatTrack.observatory import get_observatory_data, observatories
from SatTrack.visible import compute_visible
from SatTrack.tle import TLE
from SatTrack.output import OutputFile
###############################################################################

if __name__ == "__main__":
    ############################################################################
    ti = time.time()
    ############################################################################
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read("track.ini")
    ############################################################################
    # downloading tle file
    ## update this block to use pandas DataFrame :)
    satellite_brand = parser.get("satellite", "satellite")

    tle_directory = parser.get("directories", "tle")

    tle = TLE(satellite_brand=satellite_brand, directory=tle_directory)

    download = parser.getboolean("tle", "download")
    if download:
        tle_name = tle.download()
    else:
        tle_name = parser.get("tle", "name")

    tle_file_location = f"{tle_directory}/{tle_name}"
    satellites_list = tle.get_satellites_from_tle(f"{tle_file_location}")

    ############################################################################
    observatories = get_observatory_data(observatories)
    observatory = parser.get("configuration", "observatory")
    observatory_data = observatories[observatory]
    ############################################################################
    day = parser.getint("configuration", "day")
    month = parser.getint("configuration", "month")
    year = parser.getint("configuration", "year")

    window = parser.get("configuration", "window")

    time_delta = parser.getint("configuration", "delta")
    ############################################################################
    sat_alt_lower_bound = parser.getfloat(
        "satellite", "satellite_altitude_lower"
    )
    ############################################################################
    sun_zenith_lower = parser.getfloat("satellite", "sun_zenith_lower")
    sun_zenith_upper = parser.getfloat("satellite", "sun_zenith_upper")

    ############################################################################
    compute_visible_parallel = partial(
        compute_visible,
        window=window,
        observatory_data=observatory_data,
        tle_file=tle_file_location,
        year=year,
        month=month,
        day=day,
        seconds_delta=time_delta,
        satellite_altitude_lower_bound=sat_alt_lower_bound,
        sun_zenith_lower=sun_zenith_lower,
        sun_zenith_upper=sun_zenith_upper,
    )

    number_processes = parser.getint("parameters", "processes")
    with mp.Pool(processes=number_processes) as pool:
        results = pool.map(compute_visible_parallel, satellites_list)

    ###########################################################################
    output_directory = parser.get("directories", "data_output")
    output = OutputFile(results, output_directory)
    details_name = parser.get("names", "complete")
    visible_name = parser.get("names", "simple")
    output.save_data(simple_name=visible_name, full_name=details_name)
    ###########################################################################
    tf = time.time()
    print(f"Running time: {tf-ti:.2} [s]")
