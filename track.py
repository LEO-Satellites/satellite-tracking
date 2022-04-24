"""Spot visible LEO-sats with low resolution track"""
import multiprocessing as mp
import time
from configparser import ConfigParser, ExtendedInterpolation

from leosTrack.output import OutputFile
from leosTrack.tle import TLE
from leosTrack.utils.filedir import FileDirectory
from leosTrack.visible import ComputeVisibility
from observatories import observatories

###############################################################################

if __name__ == "__main__":
    ###########################################################################
    start_time = time.time()
    ###########################################################################
    CONFIG_FILE_NAME = "track"
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read(f"{CONFIG_FILE_NAME}.ini")
    ###########################################################################
    # Set output directory
    satellite_brand = parser.get("observation", "satellite")
    # observation date
    time_parameters = parser.items("time")
    time_parameters = dict(time_parameters)

    year = int(time_parameters["year"])
    month = int(time_parameters["month"])
    day = int(time_parameters["day"])
    window = time_parameters["window"]

    date = f"{year}_{month:02d}_{day:02d}_{window}"

    # Set output directory
    output_directory = parser.get("directory", "output")
    output_directory = f"{output_directory}/{satellite_brand}_{date}"
    ###########################################################################
    # downloading tle file
    print("Fetch TLE file", end="\n")

    tle = TLE(satellite_brand=satellite_brand, directory=output_directory)

    download_tle = parser.getboolean("tle", "download")

    if download_tle:

        tle_name, tle_time_stamp = tle.download()

    else:

        tle_name = parser.get("tle", "name")
        FileDirectory.check_directory(output_directory, exit_operation=True)
        FileDirectory.file_exists(f"{output_directory}/{tle_name}")

    tle_file_location = f"{output_directory}/{tle_name}"
    ###########################################################################
    print("Get list of satellites from TLE file", end="\n")
    satellites_list = tle.get_satellites_from_tle(f"{tle_file_location}")
    ###########################################################################
    # reload to get it as a tuple again
    print("Compute visibility of satellite", end="\n")

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

    number_processes = parser.getint("configuration", "processes")

    with mp.Pool(processes=number_processes) as pool:
        results = pool.map(
            compute_visibility.compute_visibility_of_satellite, satellites_list
        )

    ###########################################################################
    # Get string formats for output files
    output = OutputFile(results, output_directory)
    # Save data
    details_name = parser.get("file", "complete")
    visible_name = parser.get("file", "simple")
    output.save_data(simple_name=visible_name, full_name=details_name)
    ###########################################################################
    with open(
        f"{output_directory}/{CONFIG_FILE_NAME}.ini", "w", encoding="utf-8"
    ) as file:
        parser.write(file)
    ###########################################################################
    finish_time = time.time()
    print(f"Running time: {finish_time-start_time:.2f} [s]")
