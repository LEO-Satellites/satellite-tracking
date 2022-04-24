"""Handle output file of visible LEO-satellites"""
import pandas as pd

from leosTrack.utils.filedir import FileDirectory

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
    "DEC[dd:mm:ss]",
]
###############################################################################
class OutputFile(FileDirectory):
    """Handles data output for visible satellites"""

    def __init__(self, results: list, directory: str):
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
    def save_data(self, simple_name: str, full_name: str) -> None:
        """
        Process and save relevant data for observers in the directory
        passed to the constructor of the class

        INPUTS
            simple_name: name of file with simple observation details
            full_name: name of file with all data
        """

        print("Save data")
        self._get_data()
        super().check_directory(self.directory, exit=False)
        self._save_simple_output(simple_name)
        self._save_output(full_name)

    ###########################################################################
    def _save_simple_output(self, file_name: str) -> None:
        """
        Process and save data with simple obsevation details

        PARAMETERS
            file_name: name of file
        """

        data_frame = pd.DataFrame(
            columns=COLUMN_NAMES_SIMPLE, data=self.simple_data
        )
        #######################################################################
        # Change output format in compute visible to avoid this line of code

        data_frame["date[UT]"] = pd.to_datetime(
            data_frame["date[UT]"] + " " + data_frame["time[UT]"],
            format="%Y-%m-%d %H:%M:%Ss",
        )

        data_frame.drop(columns=["time[UT]"], inplace=True)

        #######################################################################
        # drop duplicates

        data_frame = data_frame.sample(frac=1, random_state=0)

        data_frame = data_frame.drop_duplicates(
            subset="satellite", keep="first"
        )

        data_frame.sort_values(by=["date[UT]", "satellite"], inplace=True)

        data_frame.to_csv(
            f"{self.directory}/{file_name}.txt", sep="\t", index=False
        )

    ###########################################################################
    def _save_output(self, file_name: str) -> None:
        """
        Process and save data with simple obsevation details

        PARAMETERS
            file_name: name of file
        """

        data_frame = pd.DataFrame(columns=COLUMN_NAMES, data=self.data)
        #######################################################################
        data_frame = data_frame.dropna()
        #######################################################################
        data_frame["date[UT]"] = pd.to_datetime(
            data_frame["date[UT]"] + " " + data_frame["time[UT]"],
            format="%Y-%m-%d %H:%M:%Ss",
        )

        data_frame.drop(columns=["time[UT]"], inplace=True)

        data_frame.sort_values(by=["satellite", "date[UT]"], inplace=True)

        data_frame.to_csv(
            f"{self.directory}/{file_name}.txt", sep="\t", index=False
        )

    ###########################################################################
    def _get_data(self) -> None:
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
    def _get_visible_satellites(self, results: list) -> list:
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


###############################################################################
def data_formating(
    date_obj,
    darksat_latlon,
    sat_az,
    sat_alt,
    raSAT_h,
    raSAT_m,
    raSAT_s,
    decSAT_d,
    decSAT_m,
    decSAT_s,
    sunRA,
    sunDEC,
    sun_zenith_angle,
    ang_motion,
):

    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    hour = date_obj.hour
    minute = date_obj.minute
    second = date_obj.second

    date = f"{year}-{month:02}-{day:02}"
    time = f"{hour:02}:{minute:02}:{second:02}s"

    data = [
        f"{date}",
        f"{time}",
        f"{darksat_latlon[0]:9.6f}",
        f"{darksat_latlon[1]:9.6f}",
        f"{darksat_latlon[2]:5.2f}",
        f"{sat_az:06.3f}",
        f"{sat_alt:06.3f}",
        f"{raSAT_h:02d}:{raSAT_m:02d}:{raSAT_s:05.2f}",
        f"{decSAT_d:+03d}:{decSAT_m:02d}:{decSAT_s:05.2f}",
        f"{sunRA:09.7f}",
        f"{sunDEC:09.7f}",
        f"{sun_zenith_angle:07.3f}",
        f"{ang_motion:08.3f}",
    ]

    data_simple = [
        f"{date}",
        f"{time}",
        f"{raSAT_h:02d}:{raSAT_m:02d}:{raSAT_s:05.2f}",
        f"{decSAT_d:+03d}:{decSAT_m:02d}:{decSAT_s:05.2f}",
    ]

    return data, data_simple


###############################################################################
