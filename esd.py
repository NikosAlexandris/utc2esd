# -*- coding: utf-8 -*-
"""
@author: Nikos Alexandris| Created on Wed Nov 12 16:22:18 2014
"""


"""
Calculating Earth - Sun Distance

Aquisition Time ->  Julian Day -> Earth-Sun Distance

Source: "Radiometric Use of QuickBird Imagery. Technical Note". 2005-11-07,
Keith Krause
"""

import math


"""
The acquisition time in .IMD files, uses the UTC time format:
    YYYY_MM_DDThh:mm:ss:ddddddZ;
"""
utc = '2014_11_12T16:47:08.000000Z;'
jd = 0

# helper functions ----------------------------------------------------------
# calculate Julian Day


def universal_time(hh, mm, ss):
    ut = int(hh) + (int(mm) / 60.) + (float(ss) / 3600.)
    return ut

#print "Universal Time: ", universal_time(11, 11, 11)

def julian_day(year, month, day, ut, B):
        jd = int(365.25 * (year + 4716)) + \
        int(30.6001 * (month + 1)) + \
        day + ut/24.0 + \
        B - 1525.5
        return float(jd)


def jd_to_esd(jd):  # Earth-Sun distance (U.S. Naval Observatory)
    D = float(jd) - 2451545.0
    g = 357.529 + 0.98560028 * D
    gr = math.radians(g)
    dES = 1.00014 - 0.01671 * math.cos(gr) - 0.00014 * math.cos(2 * gr)
    # check validity
    if 0.983 <= dES <= 1.017:
        return dES
    else:
        msg = "The result is an invalid Earth-Sun distance. "
        "Please review input values!"
        raise ValueError(msg)


# extract Year, Month, Day, Hours, Minutes, Seconds from UTC string
def utc_to_esd(utc):
    year = int(utc[:4])
    # Modify for Jan, Feb ---------------------------------------------------
    month = int(utc[5:7])
    if month in (1, 2):
        year -= 1
        month += 12
        print "* Modification applied for January or February"
    # -----------------------------------------------------------------------
    day = int(utc[8:10])
    hh = int(utc[11:13])
    mm = int(utc[14:16])
    ss = float(utc[17:26])

    # Universal Time
    ut = universal_time(hh, mm, ss)
#    print "Universal Time: ", ut

    # get B for Julian Day equation
    A = int(year / 100)
    B = 2 - A + int(A / 4)

    # calculate Julian Day
    jd = julian_day(year, month, day, ut, B)
#    print "Julian Day: ", jd

    dES = jd_to_esd(jd)


class AcquisitionTime:
    def __init__(self, utc):
        self.utc = utc
        self.year = int(utc[:4])
        self.month = int(utc[5:7])
        
        if self.month in (1, 2):
            self.year -= 1
            self.month += 12

        self.day = int(utc[8:10])
        self.hours = int(utc[11:13])
        self.minutes = int(utc[14:16])
        self.seconds = float(utc[17:26])

        self.ut = universal_time(self.hours, self.minutes, self.seconds)
        self.A
        self.B
        self.jd = julian_day(self.year, self.month, self.day, self.ut, self.B)
        self.esd = utc_to_esd(self.utc)
        
    def __str__(self):
        return "Acquisition time (UTC format): " + self.utc

# Exemplifying
print jd_to_esd('2014_11_12T16:47:08.000000Z;')
#
#"""
#...example, the QuickBird launch date of October 18, 2001 at 18:51:26 GMT corresponds to the Julian Day
#2452201.286.
#"""
#esd('2001_10_18T18:51:26.000000Z;')