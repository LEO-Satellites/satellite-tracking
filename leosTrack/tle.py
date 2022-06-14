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

    def __init__(self, satellite_brand: str, tle_directory: str):
        """
        Handles tle files

        PARAMETERS
            satellite_brand: Name of satellite type, e.g, oneweb
            directory: The location of the tle files
        """

        FileDirectory.__init__(self)

        self.satellite_brand = satellite_brand
        self.directory = tle_directory

    def update_tle_file(self, tle_name:str) -> None:
        """
        Make all satellite entries uniqe in tle file

        INPUT
            tle_name: name of tle file
        """

        with open(
            f"{self.directory}/{tle_name}", "r", encoding="utf8"
        ) as file:

            tle_file_lines = file.readlines()

        # raw_satellites = self.get_satellites_from_tle(
        #     f"{self.directory}/{tle_name}"
        # )
        #
        # unique_satellites = self.unique_satellites(raw_satellites[:])

        updated_tle = ""

        regular_expression = (
            r"[a-zA-Z ][a-zA-Z1-9]?.*[)]"
            r"|"
            r"[a-zA-Z ][a-zA-Z1-9]?.*[0-9a-zA-Z]"
        )

        pattern = re.compile(regular_expression)

        for idx, tle_line in enumerate(tle_file_lines):


            if idx % 3 == 0:

                satellite = pattern.findall(tle_line)[0]

                sat_id = f"{idx//3:04d}"

                tle_line = re.sub(
                    regular_expression,
                    f"{satellite}-ID-{sat_id}",
                    tle_line,
                    1
                )

            updated_tle += tle_line


        with open(
            f"{self.directory}/unique_{tle_name}", "w", encoding="utf8"
        ) as file:

            file.write(updated_tle)


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

        if satellite == "ALL":

            regular_expression = (
                r"\n[a-zA-Z ][a-zA-Z1-9]?.*[)][-]ID[-][0-9]*"
                r"|"
                r"\n[a-zA-Z ][a-zA-Z1-9]?.*[0-9a-zA-Z][-]ID[-][0-9]*"
            )

        else:

            regular_expression = (
                f"\n{satellite}.*[)][-]ID[-][0-9]*"
                f"|"
                f"\n{satellite}.*[0-9a-zA-Z][-]ID[-][0-9]*"
            )

        pattern = re.compile(regular_expression)

        with open(f"{file_location}", "r", encoding="utf-8") as tle:
            content = tle.read()

        satellites = pattern.findall(content)
        satellites = [satellite.strip("\n") for satellite in satellites]
        satellites = [satellite.strip() for satellite in satellites]

        return satellites

    @staticmethod
    def unique_satellites(satellites: list) -> list:
        """
        If a satellite is repeated in the list, it will add an
        index to defentiate them
        """

        number_of_satellites = len(satellites)

        for idx_a in range(number_of_satellites):

            for idx_b in range(idx_a, number_of_satellites):

                if satellites[idx_b] == satellites[idx_a]:

                    satellites[idx_b] = f"{satellites[idx_b]}-{idx_b:02d}"

        return satellites

    @staticmethod
    def get_time_stamp() -> str:
        """
        Returns time stamp for tle file download: "2021-10-09 16:18:16"
        """

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        time_stamp = f"{now:%Y-%m-%d_%H:%M:%S}"

        return time_stamp
