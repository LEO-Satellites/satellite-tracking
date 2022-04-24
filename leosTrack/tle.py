"""Handle operations with TLE file"""
import datetime
import re
import urllib.request

from leosTrack.utils.filedir import FileDirectory

###############################################################################
# CONSTANTS
TLE_URL = "https://celestrak.com/NORAD/elements/supplemental"
###############################################################################


class TLE(FileDirectory):

    """Handle operations with TLE file"""

    def __init__(self, satellite_brand: str, directory: str):
        """
        Handles tle files

        PARAMETERS
            satellite_brand: Name of satellite type, e.g, oneweb
            directory: The location of the tle files
        """

        FileDirectory.__init__(self)

        self.satellite_brand = satellite_brand
        self.directory = directory

    ###########################################################################
    def download(self) -> tuple:
        """
        Downloads the tle_file pass in the costructor from
        TLE_URL = f"https://celestrak.com/NORAD/elements/supplemental"

        OUTPUTS
            string with name of the tle file in the format
                "tle_{satellite_brand}_{time_stamp}.txt".
                time_stamp -> "%Y-%m-%d %H:%M:%S"
                example: "tle_oneweb_2021-10-09 16:18:16.txt"
        """

        tle_query = f"{TLE_URL}/{self.satellite_brand}.txt"

        time_stamp = self.get_time_stamp()
        tle_file_name = f"tle_{self.satellite_brand}_{time_stamp}.txt"

        super().check_directory(directory=self.directory)

        urllib.request.urlretrieve(
            tle_query, f"{self.directory}/{tle_file_name}"
        )

        return tle_file_name, time_stamp

    def get_satellites_from_tle(self, file_location: str) -> list:
        """
        Retrieves the names of satellites present in tle file.
        The tle file must be stored locally.

        PARAMETERS
            file_location: path of the tle file

        RETURNS
            list with all the sattelites available in tle file
            example: [oneweb-000, ...]
        """

        super().file_exists(file_location, exit_operation=True)

        # oneweb -> ONEWEB
        satellite = self.satellite_brand.upper()

        regular_expression = f"{satellite}-[0-9]*.*\)|{satellite}.[0-9]*"
        pattern = re.compile(regular_expression)

        with open(f"{file_location}", "r", encoding="utf-8") as tle:
            content = tle.read()

        satellites = pattern.findall(content)

        return satellites

    @staticmethod
    def get_time_stamp() -> str:
        """
        Returns time stamp for tle file download: "2021-10-09 16:18:16"
        """

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        time_stamp = f"{now:%Y-%m-%d_%H:%M:%S}"

        return time_stamp
