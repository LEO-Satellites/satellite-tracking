#! /usr/bin/env python3
import multiprocessing as mp
import os
import sys
import time
from configparser import ConfigParser, ExtendedInterpolation
from functools import partial

###############################################################################
import numpy as np
import pandas as pd

###############################################################################
from observatories import observatories
from SatTrack.output import OutputFile
from SatTrack.tle import TLE
from SatTrack.visible import ComputeVisibility

###############################################################################

if __name__ == "__main__":
    ###########################################################################
    start_time = time.time()
    ###########################################################################
    config_file_name = "track.ini"
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read(f"{config_file_name}")
    ###########################################################################
    satellite_brand = parser.get("observation", "satellite")
    # date
    time_parameters = parser.items("time")
    time_parameters = dict(time_parameters)
    year = int(time_parameters["year"])
    month = int(time_parameters["month"])
    day = int(time_parameters["day"])
    window = time_parameters["window"]
    date = f"{year}_{month:02d}_{day:02d}_{window}"
    # Set output directory
    output_directory = parser.get("directory", "data_output")
    output_directory = f"{output_directory}/{satellite_brand}_{date}"
    ###########################################################################

    # downloading tle file
    print("Fetch TLE file", end="\n")

    # satellite_brand = parser.get("observation", "satellite")
    # tle_directory = parser.get("directory", "tle")

    # tle = TLE(satellite_brand=satellite_brand, directory=tle_directory)
    tle = TLE(satellite_brand=satellite_brand, directory=output_directory)

    download_tle = parser.getboolean("tle", "download")

    if download_tle:
        tle_name, tle_time_stamp = tle.download()
    else:
        tle_name = parser.get("tle", "name")

    # tle_file_location = f"{tle_directory}/{tle_name}"
    # satellites_list = tle.get_satellites_from_tle(f"{tle_file_location}")
    tle_file_location = f"{output_directory}/{tle_name}"
    satellites_list = tle.get_satellites_from_tle(f"{tle_file_location}")
    ###########################################################################
    time_parameters = parser.items("time")

    observatory_name = parser.get("observation", "observatory")
    observatory_data = observatories[f"{observatory_name}"]

    observations_constraints = parser.items("observation")

    compute_visibility = ComputeVisibility(
        custom_window=False,
        time_parameters=time_parameters,
        observatory_data=observatory_data,
        observation_constraints=observations_constraints,
        tle_file_location=tle_file_location,
    )

    print("Compute visibility of satellite")

    number_processes = parser.getint("configuration", "processes")

    with mp.Pool(processes=number_processes) as pool:
        results = pool.map(
        compute_visibility.compute_visibility_of_satellite,
        satellites_list
    )

    ###########################################################################
    # Get string formats for output files
    output = OutputFile(results, output_directory)
    # Save data
    details_name = parser.get("file", "complete")
    visible_name = parser.get("file", "simple")
    output.save_data(simple_name=visible_name, full_name=details_name)
    ###########################################################################
    with open(f"{output_directory}/{config_file_name}", "w") as config_file:
        parser.write(config_file)
    # save tle file too if person wants to reproduce code1
    print(f"{tle_name}")
    # with open(f"{tle_file_location}", "r+" ) as file:
    #     file.write(f"{output_directory}/tel_file")
    ###########################################################################
    finish_time = time.time()
    print(f"Running time: {finish_time-start_time:.2f} [s]")
