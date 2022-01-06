import sys
import datetime
import multiprocessing as mp

import ephem
import numpy as np
import pyorbital
from pyorbital.orbital import Orbital

from SatTrack.superclasses import FileDirectory
from SatTrack.format import format
from SatTrack.units import ConvertUnits
from SatTrack.observatory import get_observatory_data

###############################################################################
# def init_compute_visibility_worker(input_counter: mp.Value):
#     """
#     Initialize worker for compute or be simulate
#
#     PARAMETERS
#         counter: counter with locl method to keep track of satellite
#             visibility computation
#     """
#     global counter
#
#     counter = input_counter
###############################################################################
convert = ConvertUnits()


class ComputeVisibility(FileDirectory):
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

            time_parameters: contains parameters of the observation date
                {
                    'year': year of observation, eg, '2021'
                    'month': month of observation, eg, '11'
                    'day': day of observation, eg, '25'
                    'delta': time delta for computation in seconds, eg,
                        '60'
                    'window': observation done either 'morning'
                        or 'evening'
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
                    # considered visible, in [units]

                    'lowest_altitude_satellite': '30' # degree

                    # if sun zenith is between these bounds satelite
                    # is considered baseurl

                    'sun_zenith_lowest': '97' # degree
                    'sun_zenith_highest': '114' # degree
                }

            tle_file_location: path to tle file used to compute visibility
        """
        #######################################################################
        window = time_parameters["window"]

        if window not in ["morning", "evening"]:
            print(f'window keyword must be of either "morning" or "evening"')
            sys.exit()
        #######################################################################

        self.time_parameters = self._set_time_parameters(time_parameters)

        self.observatory_data = self._set_observatory_data(observatory_data)

        self.constraints = observation_constraints

        self.tle_file_location = tle_file_location

        self.observer = None

    ###########################################################################
    def compute_visibility_of_satellite(self, satellite_name: str) -> list:
        """
        PARAMETERS
            satellite: name of a satellite, eg, "ONEWEB-0008"

        OUTPUT
            list with visible satellites data ?
        """

        ######################################################################
        self._set_observer()
        satellite = self._set_dark_satellite(satellite_name)
        ######################################################################
        # if time_delta = 60, then it will move minute by minute
        time_step_in_seconds = self.time_parameters["delta"]

        time_delta_in_seconds = datetime.timedelta(
            seconds=time_step_in_seconds
        )

        [hour, day] = self.set_window()

        date_time = datetime.datetime(
            year=self.time_parameters["year"],
            month=self.time_parameters["month"],
            day=day,
            hour=hour,
            minute=0,
            second=0,
        )

        previous_satellite_azimuth = 0
        previous_satellite_altitude = 0
        ######################################################################
        visible_satellite_data = []
        ######################################################################
        # 12 because time windows are of 12 hours
        number_iterations = (12 * 60 * 60) / time_step_in_seconds
        number_iterations = range(int(number_iterations))

        print(f"Compute visibility of: {satellite_name}")

        for time_step in number_iterations:
            ###################################################################
            # compute current latitude, longitude of the satellite's
            # footprint and its current orbital altitude
            try:
                satellite_lon_lat_alt = satellite.get_lonlatalt(
                    date_time
                )
            except:
                return None
            ###################################################################
            # uses the observer coordinates to compute the satellite azimuth
            # and elevation, negative elevation implies satellite is under
            # the horizon. altitude must be in kilometers

            observatory_longitude = self.observatory_data["longitude"]
            observatory_latitude = self.observatory_data["latitude"]
            observatory_altitude = self.observatory_data["altitude"] / 1000.0

            satellite_azimuth, satellite_altitude = satellite.get_observer_look(
                date_time,
                observatory_longitude,
                observatory_latitude,
                observatory_altitude,
            )
            ###################################################################
            # gets the Sun's RA and DEC at the time of observation
            sun_RA, sun_DEC = pyorbital.astronomy.sun_ra_dec(date_time)

            sun_RA = convert.RA_in_radians_to_hours(RA=sun_RA)
            sun_DEC = convert.radians_to_degrees(radians=sun_DEC)
            ###################################################################
            self._update_observer_date(date_time)

            [
                [ra_satellite_h, ra_satellite_m, ra_satellite_s],
                [dec_satellite_d, dec_satellite_m, dec_satellite_s],
            ] = self._get_satellite_RA_DEC_from_azimuth_and_altitude(
                satellite_azimuth, satellite_altitude
            )
            ###################################################################
            lowest_altitude_satellite = float(
                self.constraints["lowest_altitude_satellite"]
            )

            ###################################################################
            sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(
                date_time, observatory_longitude, observatory_latitude
            )

            sun_zenith_highest = float(self.constraints["sun_zenith_highest"])
            sun_zenith_lowest = float(self.constraints["sun_zenith_lowest"])
            ###################################################################

            check_altitude = satellite_altitude > lowest_altitude_satellite
            check_sun_zenith = sun_zenith_lowest < sun_zenith_angle
            check_sun_zenith *= sun_zenith_angle < sun_zenith_highest
            # Add bool() to avoid having np.bool_ type. This way, I can have
            # if satellite_is_visible is True:
            satellite_visibility = bool(check_altitude and check_sun_zenith)

            if satellite_visibility is True:
                print(f"{satellite_name} is visible")
                ###############################################################
                # compute the change in AZ and ALT of the satellite position
                # between current and previous observation
                ## difference in azimuth arcsecs
                delta_azimuth = (
                    satellite_azimuth - previous_satellite_azimuth
                ) * 3600
                ## difference in altitude in arcsecs
                delta_altitude = (
                    satellite_altitude - previous_satellite_altitude
                ) * 3600
                ###############################################################
                dt = time_delta_in_seconds.total_seconds()
                angular_velocity = (
                    np.sqrt(delta_azimuth ** 2 + delta_altitude ** 2) / dt
                )

                data_str, data_str_simple = format.data_formating(
                    date_time,
                    satellite_lon_lat_alt,
                    satellite_azimuth,
                    satellite_altitude,
                    ra_satellite_h,
                    ra_satellite_m,
                    ra_satellite_s,
                    dec_satellite_d,
                    dec_satellite_m,
                    dec_satellite_s,
                    sun_RA,
                    sun_DEC,
                    sun_zenith_angle,
                    angular_velocity,
                )
                ###############################################################
                visible_satellite_data.append([data_str, data_str_simple])
            ###################################################################
            # current position, time as the "previous" for next observation
            previous_satellite_azimuth = satellite_azimuth
            previous_satellite_altitude = satellite_altitude
            date_time += time_delta_in_seconds
        #####################################################################
        if len(visible_satellite_data) > 0:
            return [[satellite] + data for data in visible_satellite_data]
        return [time_delta_in_seconds, date_time]

    ###########################################################################
    def _get_satellite_RA_DEC_from_azimuth_and_altitude(
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

        RA_satellite, DEC_satellite = self.observer.radec_of(
            np.radians(satellite_azimuth), np.radians(satellite_altitude)
        )
        ##################################################################
        [
            ra_satellite_h,
            ra_satellite_m,
            ra_satellite_s,
        ] = convert.RA_in_radians_to_hh_mm_ss(RA=RA_satellite)

        [
            dec_satellite_d,
            dec_satellite_m,
            dec_satellite_s,
        ] = convert.DEC_in_radians_to_dd_mm_ss(DEC=DEC_satellite)

        return [
            [ra_satellite_h, ra_satellite_m, ra_satellite_s],
            [dec_satellite_d, dec_satellite_m, dec_satellite_s],
        ]

    ###########################################################################
    def _set_time_parameters(self, time_parameters: dict) -> dict:
        """
        Convert strings to numeric values in time parameters dictionary

        PARAMETERS
            time_parameters: contains parameters of the observation date
                {
                    'year': '2021'
                    'month': '11'
                    'day': '25'
                    'delta': '60'
                    'window': either 'morning' or 'evening'
                }
        OUTPUTS
            time_parameters: contains parameters of the observation date
                {
                    'year': 2021
                    'month': 11
                    'day': 25
                    'delta': 60
                    'window': either 'morning' or 'evening'
                }
        """

        time_parameters["year"] = int(time_parameters["year"])
        time_parameters["month"] = int(time_parameters["month"])
        time_parameters["day"] = int(time_parameters["day"])
        time_parameters["delta"] = float(time_parameters["delta"])

        return time_parameters

    ###########################################################################
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

        observatory_name = self.observatory_data["name"]
        print(f"Set observer: {observatory_name}")
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
    def _set_observatory_data(self, data_observatory: dict) -> dict:
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

            if type(parameters_values) == list:
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

        return update_format

    ###########################################################################
    def _update_observer_date(self, date_time: datetime.datetime) -> None:

        self.observer.date = ephem.date(date_time)

    ###########################################################################
    def set_window(self) -> list:
        """
        Set day and  hour of observation according to time zone

        OUTPUTS

            [hour: int, day: int]:
        """

        window = self.time_parameters["window"]
        day = self.time_parameters["day"]
        observatory_time_zone = self.observatory_data["tz"]

        if (window == "morning") and (observatory_time_zone < 0):

            day -= 1

        hour = self._set_hour(window, observatory_time_zone)

        return [hour, day]

    ###########################################################################
    def _set_hour(self, window: str, observatory_time_zone: int) -> int:

        """
        Set hour of observation according to the time zone of the observer
        and the time window in wchich the observation will be made

        PARAMETERS
            window: either 'evening' or 'morning'
            observatory_time_zone: time zone of observatory

        OUTPUTS
            hour
        """

        if window == "evening":

            hour = 12 + observatory_time_zone

        elif window == "morning":

            hour = 0 + observatory_time_zone

        if hour >= 24:
            hour -= 24

        elif hour < 0:
            hour += 24

        return hour

    ###########################################################################
