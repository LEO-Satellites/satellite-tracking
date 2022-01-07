#! /usr/bin/env python3
from configparser import ConfigParser, ExtendedInterpolation
from functools import partial
import multiprocessing as mp
import os
import sys
import time

###############################################################################
import numpy as np
import pandas as pd

###############################################################################
from observatories import observatories
from SatTrack.visible import ComputeVisibility
from SatTrack.tle import TLE
from SatTrack.output import OutputFile

###############################################################################

if __name__ == "__main__":
    ###########################################################################
    ti = time.time()
    ###########################################################################
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read("track.ini")
    ###########################################################################
    # downloading tle file
    print("Fetch TLE file", end="\n")

    satellite_brand = parser.get("observation", "satellite")
    tle_directory = parser.get("directories", "tle")

    tle = TLE(satellite_brand=satellite_brand, directory=tle_directory)

    download_tle = parser.getboolean("tle", "download")

    if download_tle:
        tle_name = tle.download()
    else:
        tle_name = parser.get("tle", "name")

    tle_file_location = f"{tle_directory}/{tle_name}"
    satellites_list = tle.get_satellites_from_tle(f"{tle_file_location}")

    ###########################################################################
    time_parameters = dict(parser.items("time"))

    observatory_name = parser.get("observation", "observatory")
    observatory_data = observatories[f"{observatory_name}"]

    observations_constraints = dict(parser.items("observation"))

    compute_visibility = ComputeVisibility(
        time_parameters=time_parameters,
        observatory_data=observatory_data,
        observation_constraints=observations_constraints,
        tle_file_location=tle_file_location,
    )

    print("Compute visibility of satellite")

    results = compute_visibility.compute_visibility_of_satellite(
        satellite_name="ONEWEB-0231"
    )
    print(results[0])
    # number_processes = parser.getint("parameters", "processes")

   #  with mp.Pool(processes=number_processes) as pool:
    #     results = pool.map(
    #     compute_visibility.compute_visibility_of_satellite,
    #     satellites_list
    # )

   #  output_directory = parser.get("directories", "data_output")
    # output = OutputFile(results, output_directory)
    # details_name = parser.get("names", "complete")
    # visible_name = parser.get("names", "simple")
    # output.save_data(simple_name=visible_name, full_name=details_name)
    # ###########################################################################
    # tf = time.time()
    # print(f"Running time: {tf-ti:.2} [s]")
