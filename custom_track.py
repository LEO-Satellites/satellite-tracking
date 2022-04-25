"""Track LEO-sats with a custom time windows """
import multiprocessing as mp
import time
from configparser import ConfigParser, ExtendedInterpolation

from leosTrack.output import OutputFile
from leosTrack.tle import TLE
from leosTrack.visible import ComputeVisibility

###############################################################################
from observatories import observatories

###############################################################################
if __name__ == "__main__":
    ###########################################################################
    start_time = time.time()
    ###########################################################################
    CONFIG_FILE_NAME = "custom_track"
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
    day = int(time_parameters["start_day"])

    start_hour = int(time_parameters["start_hour"])
    start_minute = int(time_parameters["start_minute"])
    finish_hour = int(time_parameters["finish_hour"])
    finish_minute = int(time_parameters["finish_minute"])

    date = (
        f"{year}-{month:02d}-{day:02d}_"
        f"{start_hour:02d}:{start_minute:02d}_"
        f"{finish_hour:02d}:{finish_minute:02d}"
    )

    # Set output directory
    output_directory = parser.get("directory", "output")
    output_directory = f"{output_directory}/{satellite_brand}_{date}"
    ###########################################################################
    # downloading tle file
    print("Fetch TLE file", end="\n")

    tle = TLE(satellite_brand=satellite_brand, directory=output_directory)

    download_tle = parser.getboolean("tle", "download")

    if download_tle:
        tle_name, time_stamp = tle.download()
    else:
        tle_name = parser.get("tle", "name")

    tle_file_location = f"{output_directory}/{tle_name}"
    ###########################################################################
    time_parameters = parser.items("time")

    observatory_name = parser.get("observation", "observatory")
    observatory_data = observatories[f"{observatory_name}"]

    observations_constraints = parser.items("observation")

    compute_visibility = ComputeVisibility(
        custom_window=True,
        time_parameters=time_parameters,
        observatory_data=observatory_data,
        observation_constraints=observations_constraints,
        tle_file_location=tle_file_location,
    )

    number_processes = parser.getint("configuration", "processes")

    visible_satellites = parser.get("observation", "satellites")
    visible_satellites = visible_satellites.split("\n")
    print(output_directory)
    # import sys
    # sys.exit()
    with mp.Pool(processes=number_processes) as pool:
        results = pool.map(
            compute_visibility.compute_visibility_of_satellite,
            visible_satellites,
        )
    ##########################################################################
    output = OutputFile(results, output_directory)
    details_name = parser.get("file", "complete")
    visible_name = parser.get("file", "simple")
    output.save_data(simple_name=visible_name, full_name=details_name)
    ##########################################################################
    with open(
        f"{output_directory}/{CONFIG_FILE_NAME}.ini", "w", encoding="utf-8"
    ) as file:

        parser.write(file)
    ##########################################################################
    finish_time = time.time()
    print(f"Running time: {finish_time-start_time:.2f} [s]")
