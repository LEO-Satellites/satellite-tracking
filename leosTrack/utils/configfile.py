import os
import sys

###############################################################################
class ConfigurationFile:
    """Manage common operation with configuration files.
    For instance:

        [parameters]
        metric = mse, lp, mad

    when reading metric I can inmediately get it as a list if looping
    is needed in addition, I can get a whole section in the configuration
    file as a dictionary and do the necessary transformation to each key,
    value pair

    """

    def __init__(self):
        pass

    ###########################################################################
    def section_to_dictionary(
        self,
        section_items: tuple,
        split_variable: bool = False,
        value_separators: list = ["\n"],
    ) -> dict:
        """
        Converts a section in the configuration file to a dictionary.
        WARNING: all values are strings.
        If there is a variable with multiple lines, the values of the
        associated key in the dictionary would be a list

        PARAMETERS
            section_items: items in a section of the configuration file

        OUTPUTS
            section_dictionary: items transformed
        """
        section_dictionary = dict(section_items)

        if split_variable is True:

            for key, value in section_dictionary.items():

                for separator in value_separators:

                    if separator in value:

                        value = value.split(separator)
                        section_dictionary[key] = value
        #######################################################################
        section_dictionary = self._transform_values_in_dictionary(
            section_dictionary
        )

        return section_dictionary

    ###########################################################################
    def entry_to_list(self, entry: str, entry_type: str) -> list:
        """

        PARAMETERS

            entry: a coma separated string
                architecture: 100, 50, 5, 50, 100

            entry_type: either float, int or bool

        OUTPUTS
            entry_list: list of elements in entry with the type
                100, 50, 5, 50, 100 --> [100, 50, 5, 50, 100]
        """
        pass

    ###########################################################################
    def _transform_values_in_dictionary(self, dictionary: dict):

        for key, value in dictionary.items():

            is_list = type(value) is type([])
            value = self._transform_values(value, is_list)

            dictionary[key] = value

        return dictionary

    ###########################################################################
    def _transform_values(self, items: str, is_list: bool = False):

        if is_list is True:

            new_items = []

            for string in items:

                value = self._get_value_from_string(string)
                new_items.append(value)

            return new_items

        return self._get_value_from_string(items)

    ###########################################################################
    def _get_value_from_string(self, string: str):

        """
        Get value from string variable, could be: bool, str, int or float
        """
        string = string.strip()
        #######################################################################
        # check for bool
        if (string == "True") or (string == "False"):

            return string == "True"

        #######################################################################
        # check for float
        is_float = True
        if "." in string:
            for val in string.split("."):
                is_float = is_float and val.isnumeric()

            if is_float is True:
                return float(string)

        # check for int
        if string.isnumeric():
            return int(string)

        return string


###############################################################################
class FileDirectory:
    """Handle common operations with files and directories"""

    def __init__(self):
        pass

    ###########################################################################
    def check_directory(self, directory: str, exit: bool = False) -> None:
        """
        Check if a directory exists, if not it creates it or
        exits depending on the value of exit
        """

        if not os.path.exists(directory):

            if exit:
                print(f"Directory {diretory} NOT FOUND")
                print("Code cannot execute")
                sys.exit()

            os.makedirs(directory)

    ###########################################################################
    def file_exists(self, location: str, exit: bool = False) -> bool:
        """
        Check if a location is a file, if not exits depending
        on the value of exit
        """

        file_exists = os.path.isfile(location)

        if not file_exists:

            file_name = location.split("/")[-1]

            if exit:
                print(f"File {file_name} NOT FOUND!")
                print("Code cannot execute")
                sys.exit()

            return file_exists

        return file_exists


###############################################################################
