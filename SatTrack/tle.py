import datetime
import os
import re
import sys
import urllib

###############################################################################
# CONSTANTS
TLE_URL = f"https://celestrak.com/NORAD/elements/supplemental"
###############################################################################
class TLE:
    def __init__(self,
        # configuration: "dictionary",
        satellite_brand: "str",
        directory: "str",
        file_name: "str",
    ):

        self.satellite_brand = satellite_brand
        self.directory = directory
    ###########################################################################
    def download(self):

        tle_query = f"{TLE_URL}/{self.satellite_brand}.txt"

        time_stamp = self._get_time_stamp()
        tle_file_name = f"tle_{self.satellite_brand}_{time_stamp}.txt"


        self._check_directory(directory=self.directory, exit=False)

        urllib.request.urlretrieve(
                                    tle_query,
                                    f"{self.directory}/{tle_file_name}"
                                )

        return tle_file_name
    ###########################################################################
    def get_satellites_from_tle(self, file_location: "str")->"list":
        """
        Read tle file

        PARAMETERS

        file_location: path of the tle file
        satellite: Name of the satellite in uppercase, ONEWEB

        RETURNS

        list with all the sattelites available in the tle file
        """

        self._check_file(file_location, exit=True)

        satellite = self.satellite_brand.upper()

        regular_expression = f"{satellite}-[0-9]*.*\)|{satellite}.[0-9]*"
        pattern = re.compile(regular_expression)


        with open(f"{file_location}", "r") as tle:
            content = tle.read()

        satellites = pattern.findall(content)

        return satellites
    ###########################################################################
    def _get_time_stamp(self):

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        time_stamp = f"{now:%Y-%m-%d %H:%M:%S}"
        return time_stamp
    ###########################################################################
    def _check_directory(self, directory: "str", exit: "bool"):

        if not os.path.exists(directory):

            if exit:
                sys.exit()

            os.makedirs(directory)

    ###########################################################################
    def _check_file(self, file_location: "str", exit: "bool"):

        if not os.path.exists(file_location):

            if exit:
                print(f"NOT FOUND: {file_location}")
                print(f"Program cannot execute width out this file")
                sys.exit()
    ###########################################################################
