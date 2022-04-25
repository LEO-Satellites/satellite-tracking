"Handle conversion of units"

from typing import List
import numpy as np


class ConvertUnits:
    """Handle common used conversion of units"""

    def __init__(self):
        pass

    @staticmethod
    def right_ascension_in_radians_to_hours(right_ascension: float) -> float:
        """
        Converts right_ascension from degress to hours

        PAright_ascensionMETERS
            right_ascension: right_ascension in radians ??

        OUTPUTS
            right_ascension_in_hours: right_ascension in hours

        """
        right_ascension_in_degrees = np.rad2deg(right_ascension)

        if right_ascension_in_degrees < 0:
            right_ascension_in_degrees += 360

        right_ascension_in_hours = right_ascension_in_degrees * (24.0 / 360.0)

        return right_ascension_in_hours

    def right_ascension_in_radians_to_hh_mm_ss(
        self, right_ascension: float
    ) -> List[float]:
        """
        Converts right_ascension in radians to hh:mm:ss.sss

        PAright_ascensionMETERS

        OUTPUTS
            [hh, mm, ss]
                hh: int value of hours
                mm: int value of minutes
                ss: int value of seconds
        """

        hours = self.right_ascension_in_radians_to_hours(right_ascension)
        minutes = (hours - int(hours)) * 60.0
        seconds = (minutes - int(minutes)) * 60

        hours, minutes = int(hours), int(minutes)
        return [hours, minutes, seconds]

    @staticmethod
    def declination_in_radians_to_dd_mm_ss(declination: float) -> List[float]:
        """
        Converts declination in radians to dd:mm:ss.sss

        PAright_ascensionMETERS

        OUTPUTS
            [dd, mm, ss]
                dd: int value of degrees
                mm: int value of minutes
                ss: int value of seconds
        """
        declination_in_degrees = np.rad2deg(declination)

        if declination_in_degrees < 0:
            declination_sign = -1
            declination_in_degrees = abs(declination_in_degrees)
        else:
            declination_sign = 1

        minutes = (declination_in_degrees - int(declination_in_degrees)) * 60.0

        seconds = (minutes - int(minutes)) * 60

        declination, minutes = [
            declination_sign * int(declination_in_degrees),
            int(minutes),
        ]

        return [declination, minutes, seconds]
