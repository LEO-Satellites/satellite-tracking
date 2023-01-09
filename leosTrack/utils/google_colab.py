"""
This module contains functions to run the program in Google Colab.
"""

import configparser
from typing import List


def check_config_file(
    config: configparser.ConfigParser
) -> List[dict]:
    """
    Check if the config file is in the correct format.

    INPUTS:
        config: configuration file read by configparser module

    OUTPUTS:
        time_dict: dictionary with time parameters
        observation_dict: dictionary with observation parameters
        tle_dict: dictionary with TLE parameters
        directory_dict: dictionary with directory parameters
        file_dict: dictionary with file parameters
        configuration_dict: dictionary with configuration parameters
    """

    # Create a dictionary for each section
    time_dict = dict(config['time'])
    observation_dict = dict(config['observation'])
    tle_dict = dict(config['tle'])
    directory_dict = dict(config['directory'])
    file_dict = dict(config['file'])
    configuration_dict = dict(config['configuration'])

    # Convert non numeric values to strings
    time_dict = {key: str(value) for key, value in time_dict.items()}
    observation_dict = {
        key: str(value) for key, value in observation_dict.items()
    }
    tle_dict = {key: str(value) for key, value in tle_dict.items()}
    directory_dict = {key: str(value) for key, value in directory_dict.items()}
    file_dict = {key: str(value) for key, value in file_dict.items()}
    configuration_dict = {
        key: str(value) for key, value in configuration_dict.items()
    }

    return [
        time_dict,
        observation_dict,
        tle_dict,
        directory_dict,
        file_dict,
        configuration_dict,
    ]
