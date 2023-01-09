# General overview: running track.py in the cloud with **Google Colab** 

* The code enables parallel processing in the **Google Colab** environment, allowing it to utilize multiple cores to speed up computations.
* It clones the **[satellite-tracking repository](https://github.com/CLEOsat-group/satellite-tracking)** from GitHub and installs the required dependencies listed in the **requirements.txt** file.
* It reads the contents of the **track.ini** configuration file and parses it using the ``configparser`` library.
* It updates the values of various sections in the **track.ini** file, including the time, observation, tle, directory, file, and configuration sections.
* It writes the modified configuration back to the **track.ini** file.
* It runs the **track.py** script to perform the satellite tracking.
* It creates a zip archive of the output which in **Google Colab** is located in the `/content/satellite-tracking/output/` directory and downloads it to the user's computer.