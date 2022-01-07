import os
import sys

###############################################################################
class FileDirectory:
    """Handle common operations with files and directories"""

    def __init__(self):
        pass

    ###########################################################################
    def check_directory(
        self, directory: str, exit: bool = False
    ) -> None:
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
