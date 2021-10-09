import os
import urllib
from datetime import datetime, timezone

################################################################################
def time_stamp():

    date = datetime.now(tz=timezone.utc)
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second

    stamp = (
        f"{year}_{month:02}_{day:02}_" f"{hour:02}h_{minute:02}m_{second:02}s"
    )

    return stamp


################################################################################
################################################################################
def download_tle(satellite_brand: "str", tle_dir: "str"):

    sat_tle_url = (
        f"https://celestrak.com/NORAD/elements/supplemental/"
        f"{satellite_brand}.txt"
    )

    tle_file = f"tle_{satellite_brand}_{time_stamp()}.txt"

    if not os.path.exists(tle_dir):
        os.makedirs(tle_dir)

    urllib.request.urlretrieve(sat_tle_url, f"{tle_dir}/{tle_file}")

    return tle_file


################################################################################
