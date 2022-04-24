"""Handle operations with files and directories"""
import os
import sys


class FileDirectory:
    """Handle common operations with files and directories"""

    def __init__(self):
        pass

    @staticmethod
    def check_directory(directory: str, exit_operation: bool = False) -> None:
        """
        Check if a directory exists, if not it creates it or
        exits depending on the value of exit_operation
        """

        if not os.path.exists(directory):

            if exit_operation:
                print(f"Directory {directory} NOT FOUND")
                print("Code cannot execute")
                sys.exit()

            os.makedirs(directory)

    @staticmethod
    def file_exists(location: str, exit_operation: bool = False) -> bool:
        """
        Check if a location is a file, if not exits depending
        on the value of exit_operation
        """

        file_exists = os.path.isfile(location)

        if not file_exists:

            file_name = location.split("/")[-1]

            if exit_operation:
                print(f"File {file_name} NOT FOUND!")
                print("Code cannot execute")
                sys.exit()

            return file_exists

        return file_exists


###############################################################################
