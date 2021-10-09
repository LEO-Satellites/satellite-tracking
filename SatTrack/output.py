import os
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

###############################################################################
# CONSTANTS
# Note angular speed of the satellite is in the AZ,EL (or AZ,ALT) frame

COLUMN_NAMES = [
    "satellite",
    "date[UT]",
    "time[UT]",
    "SatLon[deg]",
    "SatLat[deg]",
    "SatAlt[km]",
    "SatAzimuth[deg]",
    "SatElevation[deg]",
    "SatRA[hr]",
    "SatDEC[deg]",
    "SunRA[hr]",
    "SunDEC[deg]",
    "SunZenithAngle[deg]",
    "SatAngularSpeed[arcsecs/sec]",
]
COLUMN_NAMES_SIMPLE = [
    "satellite",
    "date[UT]",
    "time[UT]",
    "RA[hh:mm:ss]",
    "DEC[hh:mm:ss]",
]
###############################################################################
class OutputFile:
    """Handles data output for visible satellites"""

    def __init__(self, results: "list", directory: "str"):
        """
        PARAMETERS

            results: data from parallel computation of satellites'
                visibility in a given tle file
            directory: directory to save all the outputs    
        """

        self.results = results
        self.directory = directory

        self.data = None
        self.simple_data = None

    ###########################################################################
    def save_data(self, simple_name, full_name) -> "None":
        """
        Save relevant data for observers in the directory passed to
        the constructor of the class

        INPUTS
            simple_name: name of file with simple observation details
            full_name: name of file with all data
        """

        print("Save data")
        self._get_data()
        self._check_directory(self.directory, exit=False)
        self._save_simple_output(simple_name)
        self._save_output(full_name)

    ###########################################################################
    def _save_simple_output(self, file_name) -> "None":
        """
        Process and save data with simple obsevation details

        PARAMETERS
            file_name: name of file
        """

        data_frame = pd.DataFrame(
            columns=COLUMN_NAMES_SIMPLE, data=self.simple_data
        )
        #######################################################################
        # data_frame = data_frame.dropna()

        # Change output format in compute visible to avoid this line of code
        data_frame["date[UT]"] = pd.to_datetime(
            data_frame["date[UT]"] + " " + data_frame["time[UT]"],
            format="%Y-%m-%d %H:%M:%Ss",
        )

        data_frame = data_frame.drop(columns=["time[UT]"])

        sort_time = data_frame["date[UT]"].sort_values().index
        #######################################################################
        # drop duplicates
        data_frame = data_frame.drop_duplicates("satellite", keep="first")
        data_frame.index = range(data_frame.shape[0])
        sort_time = data_frame["date[UT]"].sort_values().index

        data_frame.iloc[sort_time].to_csv(
            f"{self.directory}/{file_name}.txt", sep="\t", index=False
        )

    ###########################################################################
    def _save_output(self, file_name) -> "None":
        """
        Process and save data with simple obsevation details

        PARAMETERS
            file_name: name of file
        """

        data_frame = pd.DataFrame(columns=COLUMN_NAMES, data=self.data)
        ###########################################################################
        data_frame = data_frame.dropna()
        ###########################################################################
        data_frame["date[UT]"] = pd.to_datetime(
            data_frame["date[UT]"] + " " + data_frame["time[UT]"],
            format="%Y-%m-%d %H:%M:%Ss",
        )

        data_frame = data_frame.drop(columns=["time[UT]"])

        sort_time = data_frame["date[UT]"].sort_values().index

        data_frame.iloc[sort_time].to_csv(
            f"{self.directory}/{file_name}.txt", sep="\t", index=False
        )

    ###########################################################################
    def _get_data(self) -> "None":
        """
        Gets list of data from visible satellites.
        Example: self.data = [[satelite, data, data],....]
        """

        visible_satellites = self._get_visible_satellites(self.results)

        self.data = []
        self.simple_data = []

        for visible_satellite in visible_satellites:

            # One satellite appears more than once depending on time_step
            for visible in visible_satellite:

                [satellite, data, simple_data] = visible

                self.data.append([satellite] + data)
                self.simple_data.append([satellite] + simple_data)

    ###########################################################################
    def _get_visible_satellites(self, results: "list") -> "list":
        """
        Get visible satellites from parallel computation

        PARAMETERS
            results: list from parallel computation.
                Visible satellites are a list, non visible is None

        OUTPUTS
            returns list with visible satellites
        """

        visible_satellites = list(filter(lambda x: x != None, results))

        return visible_satellites

    ###########################################################################
    def _check_directory(self, directory: "str", exit: "bool") -> "None":
        """
        Check if a directory exists and depending on exit parameter,
        it creates the derectory or exits the program because the
        directory is necessary for computations.

        PARAMETERS
            directory: directory location
            exit: if False, it creates the directory
        """

        if not os.path.exists(directory):

            if exit:
                sys.exit()

            os.makedirs(directory)

    ###########################################################################
    def _check_file(self, file_location: "str", exit: "bool") -> "None":
        """
        Check if a file exists and depending on exit parameter, it exits
        the program because the file is necessary for computations.

        PARAMETERS

            file_location: file location with extension
                example: /home/john/data/data.txt

            exit: if True, it exits the program
        """

        if not os.path.exists(file_location):

            if exit:
                print(f"NOT FOUND: {file_location}")
                print(f"Program cannot execute width out this file")
                sys.exit()

    ###########################################################################


###############################################################################
def output_format(
    frame: "PandasDataFrame",
    file_name: "str",
    simple: "bool",
    output_directory: "str" = "./output/output_files/",
):
    """
    PARAMETERS
        frame:
        file_name:
        simple:
        output_directory:
        save:

    OUTPUTS
        frame:
    """
    ###########################################################################
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    ###########################################################################
    frame = frame.dropna()
    ###########################################################################
    frame["date[UT]"] = pd.to_datetime(
        frame["date[UT]"] + " " + frame["time[UT]"],
        format="%Y-%m-%d %H:%M:%Ss",
    )

    frame = frame.drop(columns=["time[UT]"])

    sort_time = frame["date[UT]"].sort_values().index

    if not simple:
        frame.iloc[sort_time].to_csv(
            f"{output_directory}/{file_name}.txt", sep="\t", index=False
        )

        return frame
    ############################################################################
    frame = frame.drop_duplicates("satellite", keep="first")
    frame.index = range(frame.shape[0])
    sort_time = frame["date[UT]"].sort_values().index

    frame.iloc[sort_time].to_csv(
        f"{output_directory}/{file_name}.txt", sep="\t", index=False
    )

    return frame
    ############################################################################
    # observing_time = np.empty(len(visible_satellites))


#  for idx, visible in enumerate(visible_satellites):

#      [satellite, str, str_simple] = visible

#      obs_time = str_simple.split('\t')[1].split(':')

#      hours = float(obs_time[0])
#     if hours < 3:
#         hours += 24

#      minutes = float(obs_time[1])/60.
#     seconds = float(obs_time[2][:-1])/3600.

#      obs_time = hours + minutes + seconds

#      observing_time[idx] = obs_time
################################################################################

# obs_time_sort_ids = np.argsort(observing_time)

# for sort_id in obs_time_sort_ids:

#     [satellite, str, str_simple] = visible_satellites[sort_id]

#     with open(f'{output_dir}/{output_fname}.txt',
#              'a') as file:
#        file.write(f'{satellite}\n{str}\n')

#     with open(f'{output_dir}/{output_fname_simple}.txt',
#              'a') as file_simple:
#        file_simple.write(f'{satellite}\n{str_simple}\n')
################################################################################
# # Prepare data for DataFrame
# columns_df = ["satellite"]
#
# columns_df = columns_df + [
#     header.strip() for header in column_headers.split(",")
# ]
# # all columns nan except the satellite column
# orbital_library_crash = [np.nan for _ in columns_df[:-1]]
# ############################################################################
# data_crash_satellites = []
# data_simple_crash_satellites = []
# visible_satellites = []
#
# for satellite in results:
#
#     if satellite == None:
#
#         satellite_name = ["crash"]
#         data_crash_satellites.append(
#             satellite_name + orbital_library_crash
#         )
#         data_simple_crash_satellites.append(
#             satellite_name + orbital_library_crash[:4]
#         )
#     else:
#
#         visible_satellites.append(satellite)
# ############################################################################
# # Prepare visible satellites data frame
# data_visible_satellites = []
# data_simple_visible_satellites = []
#
# for visible in visible_satellites:
#
#     for visible_ in visible:
#
#         [satellite, data, data_simple] = visible_
#         data_visible_satellites.append([satellite] + data)
#         data_simple_visible_satellites.append([satellite] + data_simple)
# ############################################################################
# data_output_directory = parser.get("directories", "data_output")
#
# if not os.path.exists(data_output_directory):
#     os.makedirs(data_output_directory)
# ############################################################################
# # create DataFrame all data
# data_df = data_visible_satellites + data_crash_satellites
# observations_df = pd.DataFrame(columns=columns_df, data=data_df)
#
# details_name = parser.get("names", "complete")
#
# observations_df = output_format(
#     frame=observations_df,
#     file_name=details_name,
#     simple=False,
#     output_directory=data_output_directory,
# )
# ############################################################################
# # create DataFrame simple data
# columns_df = [
#     "satellite",
#     "date[UT]",
#     "time[UT]",
#     "RA[hh:mm:ss]",
#     "DEC[hh:mm:ss]",
# ]
#
# data_df = data_simple_visible_satellites  # + data_simple_crash_satellites
#
# visible_df = pd.DataFrame(columns=columns_df, data=data_df)
#
# visible_name = parser.get("names", "simple")
#
# observations_df = output_format(
#     frame=visible_df,
#     file_name=visible_name,
#     simple=True,
#     output_directory=data_output_directory,
# )
# # Modify output such I only use the df with all data :)
# ################################################################################
