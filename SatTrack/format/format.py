################################################################################
def data_formating(
    date_obj,
    darksat_latlon,
    sat_az,
    sat_alt,
    raSAT_h,
    raSAT_m,
    raSAT_s,
    decSAT_d,
    decSAT_m,
    decSAT_s,
    sunRA,
    sunDEC,
    sun_zenith_angle,
    ang_motion,
):

    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    hour = date_obj.hour
    minute = date_obj.minute
    second = date_obj.second

    date = f"{year}-{month:02}-{day:02}"
    time = f"{hour:02}:{minute:02}:{second:02}s"

    data = [
        f"{date}",
        f"{time}",
        # SatLon[deg]
        f"{darksat_latlon[0]:9.6f}",
        # SatLat[deg]
        f"{darksat_latlon[1]:9.6f}",
        f"{darksat_latlon[2]:5.2f}",
        f"{sat_az:06.3f}",
        f"{sat_alt:06.3f}",
        # f"{raSAT_h:02d}h{raSAT_m:02d}m{raSAT_s:05.3f}s",
        # f"{decSAT_d:03d}:{decSAT_m:02d}:{decSAT_s:05.3f}",
        f"{raSAT_h:02d}:{raSAT_m:02d}:{raSAT_s:05.3f}",
        f"{decSAT_d:03d}:{decSAT_m:02d}:{decSAT_s:05.3f}",
        f"{sunRA:09.7f}",
        f"{sunDEC:09.7f}",
        f"{sun_zenith_angle:07.3f}",
        f"{ang_motion:08.3f}",
    ]

    data_simple = [
        f"{date}",
        f"{time}",
        # f"{raSAT_h:02d}h{raSAT_m:02d}m{raSAT_s:05.3f}s",
        f"{raSAT_h:02d}:{raSAT_m:02d}:{raSAT_s:05.3f}",
        f"{decSAT_d:03d}:{decSAT_m:02d}:{decSAT_s:05.3f}",
    ]

    return data, data_simple


################################################################################
