from collections import defaultdict
import re
###############################################################################
def get_satellites_from_tle(file_location:'str, satellite:'str uppercase'):
    """Read tle file"""


    with open(f'{file_location}', 'r') as tle:

        content = tle.read()
        pattern = re.compile(f'{satellite}-[0-9]*')
        satellites = pattern.findall(content)

        return satellites
