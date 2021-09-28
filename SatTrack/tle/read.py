from collections import defaultdict
import re
###############################################################################
def get_satellites_from_tle(tle_location:'str', satellite:'str'):
    """
    Read tle file

    PARAMETERS

    file_location: path of the tle file
    satellite: Name of the satellite in uppercase, ONEWEB

    RETURNS

    list with all the sattelites available in the tle file
    """

    satellite = satellite.upper()
    pattern = re.compile(f'{satellite}-[0-9]*')

    with open(f'{tle_location}', 'r') as tle:
        content = tle.read()

    satellites = pattern.findall(content)
    
    return satellites
