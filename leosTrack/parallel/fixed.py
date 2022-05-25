"""
Compute visibility of satellites in parallel with shared dictionary
from multiprocessing.Manager
"""

from multiprocessing.managers import DictProxy
from leosTrack.track.fixed import FixWindow

def share_data(
    time_parameters: dict,
    observatory_data:dict,
    observation_constraints:dict,
    tle_file_location:str,
    share_visibility_data: DictProxy
):
    """Init worker shared data"""

    global track_satellite
    global visibility_data

    visibility_data = share_visibility_data

    track_satellite = FixWindow(
        time_parameters=time_parameters,
        observatory_data=observatory_data,
        observation_constraints=observation_constraints,
        tle_file_location=tle_file_location,
    )


def compute_visibility_worker(satellite_name:str):

    """worker to compute whether a satellite is visible or not"""

    track_satellite.compute_visibility_of_satellite(satellite_name)
