"""Compute visibility of LEO sats according to observation constraints"""
import datetime

import numpy as np
import pyorbital

from leosTrack import output
from leosTrack.track.visible import ComputeVisibility, CONVERT


class AdaptiveTime(ComputeVisibility):
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

    def compute_visibility_of_satellite(self, satellite_name: str) -> list:
        """
        PARAMETERS
            satellite: name of a satellite, eg, "ONEWEB-0008"

        OUTPUT
            list with visible satellites data ?
        """

        ######################################################################
        # I have to set the observer per satelitte inside this function,
        # otherwise with mp.pool the line:
        # observer = ephem.Observer()
        # cannot be serialized avoiding the parallel computation.
        # Therefore in parallel the observer will be set over and over
        self._set_observer()
        satellite = self._set_dark_satellite(satellite_name)

        start_date_time, finish_date_time = self.get_date_time_object(
            time_parameters=self.time_parameters,
            time_zone=self.observatory_data["tz"],
        )

        date_time = start_date_time

        observation_window_seconds = (
            finish_date_time - start_date_time
        ).total_seconds()

        number_of_time_steps = int(
            observation_window_seconds / self.time_delta.total_seconds()
        )
        #######################################################################
        previous_satellite_azimuth = 0
        previous_satellite_altitude = 0
        #######################################################################
        visible_satellite_data = []
        #######################################################################
        print(f"Compute visibility of: {satellite_name}", end="\r")

        for _ in range(number_of_time_steps):
            # compute current latitude, longitude of the satellite's
            # footprint and its current orbital altitude
            # satellite_lon_lat_alt = satellite.get_lonlatalt(date_time)
            # Check with jeremy what was the error that motivated this block
            try:
                satellite_lon_lat_alt = satellite.get_lonlatalt(date_time)
            except RuntimeError:
                return None
            ###################################################################
            # uses the observer coordinates to compute the satellite azimuth
            # and elevation, negative elevation implies satellite is under
            # the horizon. altitude must be in kilometers
            # satellite_azimuth, satellite_altitude = satellite_coordinates

            satellite_coordinates = satellite.get_observer_look(
                date_time,
                self.observatory_data["longitude"],
                self.observatory_data["latitude"],
                self.observatory_data["altitude"] / 1000.0,
            )
            ###################################################################
            # gets the Sun's RA and DEC at the time of observation
            # sun_right_ascension, sun_declination = sun_coordinates

            sun_coordinates = pyorbital.astronomy.sun_ra_dec(date_time)
            # convert to list and allow to update variables later on
            sun_coordinates = list(sun_coordinates)

            sun_coordinates[0] = CONVERT.right_ascension_in_radians_to_hours(
                right_ascension=sun_coordinates[0]
            )
            sun_coordinates[1] = np.rad2deg(sun_coordinates[1])
            ###################################################################
            self._update_observer_date(date_time)

            [
                satellite_ra_hms,
                satellite_dec_dms,
            ] = self.get_satellite_ra_dec_from_azimuth_and_altitude(
                satellite_coordinates[0], satellite_coordinates[1]
            )
            ###################################################################
            sun_zenith = pyorbital.astronomy.sun_zenith_angle(
                date_time,
                self.observatory_data["longitude"],
                self.observatory_data["latitude"],
            )

            satellite_visibility = self.check_visibility(
                satellite_coordinates[1], sun_zenith
            )

            if satellite_visibility is True:
                print(f"{satellite_name} is visible", end="\r")
                ###############################################################
                # compute the change in AZ and ALT of the satellite position
                # between current and previous observation
                angular_velocity = self.angular_velocity(
                    satellite_coordinates,
                    previous_satellite_azimuth,
                    previous_satellite_altitude,
                )

                data_str, data_str_simple = output.data_formating(
                    date_time,
                    satellite_lon_lat_alt,
                    satellite_coordinates[0],
                    satellite_coordinates[1],
                    satellite_ra_hms[0],
                    satellite_ra_hms[1],
                    satellite_ra_hms[2],
                    satellite_dec_dms[0],
                    satellite_dec_dms[1],
                    satellite_dec_dms[2],
                    sun_coordinates[0],
                    sun_coordinates[1],
                    sun_zenith,
                    angular_velocity,
                )
                ##############################################################
                visible_satellite_data.append([data_str, data_str_simple])
            ###################################################################
            # current position, time as the "previous" for next observation
            # previous_satellite_azimuth = satellite_azimuth
            # previous_satellite_altitude = satellite_altitude
            previous_satellite_azimuth = satellite_coordinates[0]
            previous_satellite_altitude = satellite_coordinates[1]
            date_time += self.time_delta
        #######################################################################
        if len(visible_satellite_data) > 0:
            return [[satellite_name] + data for data in visible_satellite_data]

    @staticmethod
    def get_date_time_object(time_parameters: dict, time_zone: int) -> list:
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
        start_date_time = datetime.datetime(
            year=time_parameters["year"],
            month=time_parameters["month"],
            day=time_parameters["day"],
            hour=time_parameters["hour"],
            minute=time_parameters["minute"],
            second=0,
        )

        # convert to UTC
        start_date_time += time_zone

        # define end of observation
        observing_time = datetime.timedelta(
            minutes=time_parameters["observing_time"]
        )

        finish_date_time = start_date_time + observing_time

        return start_date_time, finish_date_time
