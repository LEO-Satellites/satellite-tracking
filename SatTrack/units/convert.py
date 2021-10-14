import numpy as np

###############################################################################
"""
RA: right ascention
DEC: declination
"""
###############################################################################
class ConvertUnits:
    """Convert units"""
    def __init__(self):
        pass

    def RA_in_radians_to_hours(self, RA: "float")->"float":
        """
        Converts RA from degress to hours

        PARAMETERS
            RA: RA in radians ??

        OUTPUTS
            RA_in_hours: RA in hours

        """
        RA_in_degrees = self.radians_to_degrees(RA)

        if RA_in_degrees < 0:
            RA_in_degrees += 360

        RA_in_hours = RA_in_degrees * (24.0 / 360.0)

        return RA_in_hours
    ###########################################################################
    def radians_to_degrees(self, radians: "float")->"float":
        """Convert radians to degrees"""

        degrees = radians * 180.0 / np.pi

        return degrees

    ###########################################################################
    def RA_in_radians_to_hh_mm_ss(self, RA: "float")->"list":
        """
        Converts RA in radians to hh:mm:ss.sss

        PARAMETERS

        OUTPUTS
            [hh, mm, ss]
                hh: int value of hours
                mm: int value of minutes
                ss: int value of seconds
        """

        hours = self.RA_in_radians_to_hours(RA)

        hh = int(hours)

        minutes = (hours - hh) * 60.0
        mm = int(minutes)

        ss = (minutes - mm) * 60

        return [hh, mm, ss]


    ###########################################################################
    def DEC_in_radians_to_dd_mm_ss(self, DEC: "float")->"list":
        """
        Converts DEC in radians to dd:mm:ss.sss

        PARAMETERS

        OUTPUTS
            [dd, mm, ss]
                dd: int value of degrees
                mm: int value of minutes
                ss: int value of seconds
        """
        DEC_in_degrees = self.radians_to_degrees(DEC)

        if DEC_in_degrees < 0:
            DEC_sign = -1
            DEC_in_degrees = abs(DEC_in_degrees)
        else:
            DEC_sign = 1

        dd = int(DEC_in_degrees)

        minutes = (DEC_in_degrees - dd) * 60.0
        mm = int(minutes)

        ss = (minutes - mm) * 60

        return [dd * DEC_sign, mm, ss]

###############################################################################
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
