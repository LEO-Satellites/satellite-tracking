
"""Compute visibility of LEO sats according to observation constraints"""
import datetime
import sys

import ephem
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital

from leosTrack import output
from leosTrack.track.visible import ComputeVisibility
from leosTrack.units import ConvertUnits
from leosTrack.utils.configfile import ConfigurationFile

###############################################################################

class FixWindow(ComputeVisibility):
    """Class to compute whether a satellite is visible or not"""

    def __init__(
        self,
        time_parameters: dict,
        observatory_data: dict,
        observation_constraints: dict,
        tle_file_location: dict,
    ):
        # init parent class
        ComputeVisibility.__init__(
            self,
            time_parameters,
            observatory_data,
            observation_constraints,
            tle_file_location,
        )
    ###########################################################################
    def get_date_time_object(
        self, time_parameters: dict, time_zone: int,
    ) -> list:
        """
        INPUT
            time_parameters: check constructor
            tz: time zone of the observatory location
            constant_window: wheather the user defines a time window or if it
                is the "evening" or "morning" 12 hours slot
        OUTPUTS
            [
                start_date_time: datetime.datetime,
                finish_date_time: datetime.datetime
            ]
        """
        # define local time
        if time_parameters["window"] == "morning":
            hour = 0
        elif time_parameters["window"] == "evening":
            hour = 12
        else:
            print(f"window must be: 'morning' or 'evening'")
            sys.exit()

        start_date_time = datetime.datetime(
            year=time_parameters["year"],
            month=time_parameters["month"],
            day=time_parameters["day"],
            hour=hour,
            minute=0,
            second=0,
        )

        # convert to UTC
        start_date_time += time_zone

        finish_date_time = start_date_time + datetime.timedelta(hours=12)

        return start_date_time, finish_date_time
