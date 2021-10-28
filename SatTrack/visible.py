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
def init_compute_visibility_worker(input_counter: "mp.Value"):
    """
    Initialize worker for compute or be simulate

    PARAMETERS
        counter: counter with locl method to keep track of satellite
            visibility computation
    """
    global counter

    counter = input_counter
###############################################################################
class ComputeVisibility(FileDirectory):
    """Class to compute whether a satellite is visible or not"""

    def __init__(self,
        time_parameters: "dictionary",
        observatory_data: "dictionary",
        tle_file_location: "str",
        ):
        """
        PARAMETERS

        """
    ###########################################################################
        window = time_parameters["window"]

        if window not in ["morning", "evening"]:
            print(f'window keyword must be of either "morning" or "evening"')
            sys.exit()
    ###########################################################################

        self.time_parameters = self._set_time_parameters(time_parameters)


        self.observatory_data = self._set_observatory_data(observatory_data)

        self.tle_file_location = tle_file_location

        self.observer = None


    ###########################################################################
    # def compute_visibility_of_satellite(self):

        # if time_delta = 60, then it will move minute by minute
        # time_step_in_seconds = self.time_parameters["delta"]
        # # time_delta_in_seconds = datetime.timedelta(seconds=time_step_in_seconds)

        # [hour, day] = self.set_window()

        # date_time = datetime.datetime(
            # year=self.time_parameters["year"],
            # month=self.time_parameters["month"],
            # day=day,
            # hour=hour,
            # minute=0,
            # second=0
        # )

       #  previous_satellite_azimuth = 0
        # previous_satellite_altitude = 0
        #######################################################################
        # visible_satellite_data = []
        #######################################################################
        # number_iterations = (12 * 60 * 60) / time_step_in_seconds
        # number_iterations = range(int(number_iterations))
        # time_range = np.linspace()

        # print(f"Compute visibility of: {self.satellite}", end="\r")

        # for time_step in number_iterations:
        #     ###################################################################
        #     # computes the current latitude, longitude of the satellite's
        #     # footprint and its current orbital altitude
        #     try:
        #         darksat_latitude_logitude = darksat.get_lonlatalt(date_time)
        #     except:
        #         return None
        #     ###################################################################
        #     # uses the observer coordinates to compute the satellite azimuth
        #     # and elevation, negative elevation implies satellite is under
        #     # the horizon
        #     satellite_azimuth, satellite_altitude = darksat.get_observer_look(
        #         date_time,
        #         observatory_longitude,
        #         observatory_latitude,
        #         observatory_altitude,
        #     )
        #     ###################################################################
        #     # gets the Sun's RA and DEC at the time of observation
        #     sun_ra, sun_dec = pyorbital.astronomy.sun_ra_dec(date_time)
        #
        #     sun_RA = convert.RA_in_radians_to_hours(RA=sun_ra)
        #     sun_DEC = convert.radians_to_degrees(radians=sun_dec)
        #     ###################################################################
        #     sun_zenith_angle = pyorbital.astronomy.sun_zenith_angle(
        #         date_time, observatory_longitude, observatory_latitude
        #     )
        #     ##################################################################
        #     observer.date = ephem.date(date_time)
        #     ra, dec = observer.radec_of(
        #         np.radians(satellite_azimuth), np.radians(satellite_altitude)
        #     )
        #     ##################################################################
        #     [
        #         ra_satellite_h,
        #         ra_satellite_m,
        #         ra_satellite_s
        #     ]= convert.RA_in_radians_to_hh_mm_ss(RA=ra)
        #
        #     [
        #         dec_satellite_d,
        #         dec_satellite_m,
        #         dec_satellite_s
        #     ]= convert.DEC_in_radians_to_dd_mm_ss(DEC=dec)
        #     ###################################################################
        #     visible = (satellite_altitude > satellite_altitude_lower_bound) and (
        #         sun_zenith_lower < sun_zenith_angle < sun_zenith_upper
        #     )
        #
        #     if visible:
        #         ################################################################
        #         # compute the change in AZ and ALT of the satellite position
        #         # between current and previous observation
        #         ## difference in azimuth arcsecs
        #         delta_azimuth = (satellite_azimuth - previous_satellite_azimuth) * 3600
        #         ## difference in altitude in arcsecs
        #         delta_altitude = (satellite_altitude - previous_satellite_altitude) * 3600
        #         ###################################################################
        #         dt = time_delta.total_seconds()
        #         angular_velocity = (
        #             np.sqrt(delta_azimuth ** 2 + delta_altitude ** 2) / dt
        #         )
        #
        #         data_str, data_str_simple = format.data_formating(
        #             date_time,
        #             darksat_latitude_logitude,
        #             satellite_azimuth,
        #             satellite_altitude,
        #             ra_satellite_h,
        #             ra_satellite_m,
        #             ra_satellite_s,
        #             dec_satellite_d,
        #             dec_satellite_m,
        #             dec_satellite_s,
        #             sun_RA,
        #             sun_DEC,
        #             sun_zenith_angle,
        #             angular_velocity,
        #         )
        #         ###################################################################
        #         visible_satellite_data.append([data_str, data_str_simple])
        #     ###################################################################
        #     # current position, time as the "previous" for next observation
        #     previous_satellite_azimuth = satellite_azimuth
        #     previous_satellite_altitude = satellite_altitude
        #     date_time += time_delta
        # #####################################################################
        # if len(visible_satellite_data) > 0:
        #     return [[satellite] + data for data in visible_satellite_data]
        # return [time_delta_in_seconds, date_time]
    ###########################################################################
    def _set_time_parameters(self, time_parameters: "dictionary"):

        time_parameters["year"] = int(time_parameters["year"])
        time_parameters["month"] = int(time_parameters["month"])
        time_parameters["day"] = int(time_parameters["day"])
        time_parameters["delta"] = float(time_parameters["delta"])

        return time_parameters
    ###########################################################################
    def _set_dark_satellite(self, satellite):

        dark_satellite = Orbital(
                                    satellite,
                                    tle_file=self.tle_file_location
                                )

        return dark_satellite
    ###########################################################################
    def _set_observer(self):

        observatory_name = self.observatory_data["name"]
        print(f"Set observer: {observatory_name}")
        observer = ephem.Observer()
        observer.epoch = "2000"
        observer.pressure = 1010
        observer.temp = 15
        #######################################################################
        observatory_latitude = self.observatory_data["latitude"] # degrees
        observer.lat = np.radians(observatory_latitude)
        #######################################################################
        observatory_longitude = self.observatory_data["longitude"] # degrees
        observer.lon = np.radians(observatory_longitude)
        #######################################################################
        observer.elevation = self.observatory_data["altitude"]  # in meters
        self.observer = observer

    ###########################################################################
    def _set_observatory_data(self, data_observatory: "dictionary"):
        """
        Transform data from observatories.txt file at home.
        Degrees are positive to the east and negative to the west

        PARAMETERS
            observatory_data: contains parameters of observatory
            {
                'name': 'European Southern Observatory, La Silla',
                'longitude': [70, 43.8], # entries for [deg, ', ']
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
        for parameter_observatory, parameters_values in data_observatory.items():

            if type(parameters_values) == list:
                sign = 1 # negative to the west and positive to the east
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

                    update_format[parameter_observatory] += parameter / (60 ** idx)
                ###############################################################
                update_format[parameter_observatory] = sign * update_format[parameter_observatory]

            else:
                update_format[parameter_observatory] = parameters_values

            if parameter_observatory == "longitude":

                if update_format[parameter_observatory] > 180.0:
                    update_format[parameter_observatory] = 360 - update_format[parameter_observatory]

                else:
                    update_format[parameter_observatory] = -update_format[parameter_observatory]

        return update_format
    ###########################################################################
    # def update_observer_date(self, observer, date_time):
        # observer.date = ephem.date(date_time)
        # return observer
    ###########################################################################
    # def set_window(self)-> "list":
    #     """
    #     Set day and  hour of observation according to time zone
    #
    #     OUTPUTS
    #
    #         [hour: "int", day: "int"]:
    #             set according to time window and time zone
    #
    #             hour:
    #             day:
    #     """
    #
    #     window = self.time_parameters["window"]
    #     day = self.time_parameters["day"]
    #     observatory_time_zone = self.observatory_data["tz"]
    #
    #     if (window == "morning") and (observatory_time_zone < 0):
    #
    #         day -= 1
    #
    #     hour = self._set_hour(window,observatory_time_zone)
    #
    #     return [hour, day]
    ###########################################################################
    def _set_hour(self, window: "str",observatory_time_zone: "int")-> "int":

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

##########################################################################################################################################################
