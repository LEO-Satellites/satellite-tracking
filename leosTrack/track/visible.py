"""Compute visibility of LEO sats according to observation constraints"""
import datetime

import ephem
import numpy as np
from pyorbital.orbital import Orbital

from leosTrack.units import ConvertUnits

###############################################################################
CONVERT = ConvertUnits()


class ComputeVisibility:
    """Class to compute whether a satellite is visible or not"""

    def __init__(
        self,
        time_parameters: dict,
        observatory_data: dict,
        observation_constraints: dict,
        tle_file_location: str,
    ):
        """
        PARAMETERS

            time_parameters: parameters of the observation date
            {
                'year': year of observation, eg, 2021
                'month': month of observation, eg, 11
                'day': day of observation, eg, 25
                'delta': time step resolution in seconds, eg, 60
                'window': either 'morning' or 'evening'

                if it is for an adaptive time window:

                'year': year of observation, eg, 2021
                'month': month of observation, eg, 11
                'day': day of observation, eg, 25
                'hour': at which observation begins, e.g, 22
                'minute': at which observation begins, e.g, 30
                'observing_time': how much the observation
                    lasts, it is measure in minutes e.g, 45
                'delta': time step resolution in seconds, e.g, 0.1
            }
            observatory_data: contains parameters of observatory
            {
                'name': 'European Southern Observatory, La Silla',
                'longitude': [70, 43.8], # entries for [deg, ', ']
                'latitude': [-29, 15.4],
                'altitude': 2347.0, # in meters above sea level
                'tz': 4
            }

            observation_constraints: constrains for visibility of a satellite
            {
                'observatory': 'lasilla'
                'satellite': 'oneweb'

                # lower bound for altitude of satellite to be
                # considered visible

                'lowest_altitude_satellite': 30 # degree

                # if sun zenith is between these bounds, satellite
                # is considered be visible

                'sun_zenith_lowest': 97 # degree
                'sun_zenith_highest': 114 # degree
            }

            tle_file_location: path to tle file used to compute visibility
        """
        #######################################################################

        self.time_parameters = time_parameters
        # if time_delta = 60, then it will move minute by minute
        self.time_delta = datetime.timedelta(seconds=time_parameters["delta"])

        # from heredo:
        self.observatory_data = self.set_observatory_data(observatory_data)
        # import sys
        # sys.exit()

        self.constraints = observation_constraints

        self.tle_file_location = tle_file_location

        self.observer = None
        # self._set_observer()

    def get_satellite_ra_dec_from_azimuth_and_altitude(
        self, satellite_azimuth: float, satellite_altitude: float
    ) -> list:
        """
        Compute satellite RA [hh, mm, ss] and DEC [dd, mm, ss] using
        satellite's azimuth and altitude in degrees.

        PARAMETERS
            satellite_azimuth: [degree]
            satellite_altitude: [degree]

        OUTPUTS
            [
                [ra_satellite_h, ra_satellite_m, ra_satellite_s],
                [dec_satellite_d, dec_satellite_m, dec_satellite_s]
            ]

        """

        [
            right_ascension_satellite,
            declination_satellite,
        ] = self.observer.radec_of(
            np.radians(satellite_azimuth), np.radians(satellite_altitude)
        )
        ##################################################################
        [
            ra_satellite_h,
            ra_satellite_m,
            ra_satellite_s,
        ] = CONVERT.right_ascension_in_radians_to_hh_mm_ss(
            right_ascension=right_ascension_satellite
        )

        [
            dec_satellite_d,
            dec_satellite_m,
            dec_satellite_s,
        ] = CONVERT.declination_in_radians_to_dd_mm_ss(
            declination=declination_satellite
        )

        return [
            [ra_satellite_h, ra_satellite_m, ra_satellite_s],
            [dec_satellite_d, dec_satellite_m, dec_satellite_s],
        ]

    def compute_angular_velocity(
        self,
        satellite_coordinates: list,
        previous_satellite_azimuth: float,
        previous_satellite_altitude: float,
    ) -> float:

        delta_azimuth = (
            satellite_coordinates[0] - previous_satellite_azimuth
        ) * 3600
        # difference in altitude in arcsecs
        delta_altitude = (
            satellite_coordinates[1] - previous_satellite_altitude
        ) * 3600
        ###############################################################
        dtime = self.time_delta.total_seconds()

        angular_velocity = (
            np.sqrt(delta_azimuth ** 2 + delta_altitude ** 2) / dtime
        )

        return angular_velocity

    def check_visibility(
        self, satellite_altitude: float, sun_zenith_angle: float
    ) -> bool:

        lowest_altitude_satellite = self.constraints[
            "lowest_altitude_satellite"
        ]

        sun_zenith_highest = self.constraints["sun_zenith_highest"]
        sun_zenith_lowest = self.constraints["sun_zenith_lowest"]
        ###################################################################

        check_altitude = satellite_altitude > lowest_altitude_satellite
        check_sun_zenith = sun_zenith_lowest < sun_zenith_angle
        check_sun_zenith *= sun_zenith_angle < sun_zenith_highest
        # Add bool() to avoid having np.bool_ type. This way, I can have
        satellite_visibility = bool(check_altitude and check_sun_zenith)

        return satellite_visibility

    def _set_dark_satellite(self, satellite: str) -> Orbital:
        """
        Set dark satellite object for orbital computations

        PARAMETERS
            satellite: name of the satellite to work on that is present
                the tle_file provided for the computations, eg, "ONEWEB-0008"

        OUTPUTS
            dark_satellite: instance of class pyorbital.orbital.Orbital

        """

        dark_satellite = Orbital(satellite, tle_file=self.tle_file_location)

        return dark_satellite

    ###########################################################################
    def _set_observer(self) -> None:
        """
        Set location on earth from which the observation of dark satellites
        will be made. The observe, an instance of ephem.Observer, allows
        to compute the position of celestial bodies from the selected
        location, in this case, the observatory location
        """

        observer = ephem.Observer()
        observer.epoch = "2000"
        observer.pressure = 1010
        observer.temp = 15
        #######################################################################
        observatory_latitude = self.observatory_data["latitude"]  # degrees
        observer.lat = np.radians(observatory_latitude)
        #######################################################################
        observatory_longitude = self.observatory_data["longitude"]  # degrees
        observer.lon = np.radians(observatory_longitude)
        #######################################################################
        observer.elevation = self.observatory_data["altitude"]  # in meters
        self.observer = observer

    ###########################################################################
    @staticmethod
    def set_observatory_data(data_observatory: dict) -> dict:
        """
        Transform data from observatories.txt file at home to degree in float.
        In the original file, longitude is possitive to the west.
        In the output, longitude is negative to the west

        PARAMETERS
            observatory_data: contains parameters of observatory
            {
                'name': 'European Southern Observatory, La Silla',
                'longitude': [70, 43.8],
                'latitude': [-29, 15.4],
                'altitude': 2347.0, # in meters above sea level
                'tz': 4
            }

        OUTPUTS
            update_observatory_data: update parameters of observatory
            {
                'name': 'European Southern Observatory, La Silla',
                'longitude': -70.73,
                'latitude': -29.256666666666668,
                'altitude': 2347.0,
                'tz': 4
            }
        """
        update_format = {}
        #######################################################################
        for (
            parameter_observatory,
            parameters_values,
        ) in data_observatory.items():

            if isinstance(parameters_values, list) is True:
                sign = 1  # negative to the west and positive to the east
                update_format[parameter_observatory] = 0
                ###############################################################
                for idx, parameter in enumerate(parameters_values):

                    # parameter will be in degrees, minutes and seconds
                    # idx=0 -> degrees
                    # idx=1 -> minutes
                    # idx=2 -> seconds
                    # maybe a lamda function with map?
                    if parameter < 0:
                        sign = -1
                        parameter = abs(parameter)

                    update_format[parameter_observatory] += parameter / (
                        60 ** idx
                    )
                ###############################################################
                update_format[parameter_observatory] = (
                    sign * update_format[parameter_observatory]
                )

            else:
                update_format[parameter_observatory] = parameters_values

            if parameter_observatory == "longitude":

                if update_format[parameter_observatory] > 180.0:
                    update_format[parameter_observatory] = (
                        360 - update_format[parameter_observatory]
                    )

                else:
                    update_format[parameter_observatory] = -update_format[
                        parameter_observatory
                    ]

        update_format["tz"] = datetime.timedelta(hours=data_observatory["tz"])
        return update_format

    ###########################################################################
    def _update_observer_date(self, date_time: datetime.datetime) -> None:

        self.observer.date = ephem.date(date_time)

    ###########################################################################
