import numpy as np

################################################################################
def ra_to_hours(ra):
    ra = ra * 180.0 / np.pi

    if ra < 0:
        ra += 360

    ra = ra * (24.0 / 360.0)

    return ra


################################################################################
def radians_to_deg(radians):

    deg = radians * 180.0 / np.pi

    return deg


################################################################################
def ra_to_hh_mm_ss(ra):
    # converts the RA to hh:mm:ss.sss

    hrs = ra_to_hours(ra)

    hh = int(hrs)

    mins = (hrs - hh) * 60.0
    mm = int(mins)

    ss = (mins - mm) * 60

    return hh, mm, ss


################################################################################
def dec_to_dd_mm_ss(dec):
    # converts the DEC to dd:mm:ss
    dec = radians_to_deg(dec)

    if dec < 0:
        dec_sign = -1
        dec = abs(dec)
    else:
        dec_sign = 1

    dd = int(dec)

    mins = (dec - dd) * 60.0
    mm = int(mins)

    ss = (mins - mm) * 60

    return dd * dec_sign, mm, ss


################################################################################
