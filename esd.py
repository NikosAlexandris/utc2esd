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


# helper functions ----------------------------------------------------------


def extract_time_elements(utc):
    at = {}
    # extract Year, Month, Day, Hours, Minutes, Seconds from UTC string
    at['year'] = int(utc[:4])
    # Modify for Jan, Feb ---------------------------------------------------
    at['month'] = int(utc[5:7])
    if at['month'] in (1, 2):
        at['year'] -= 1
        at['month'] += 12
        print "* Modification applied for January or February"
    # -----------------------------------------------------------------------
    at['day'] = int(utc[8:10])
    at['hours'] = int(utc[11:13])
    at['minutes'] = int(utc[14:16])
    at['seconds'] = float(utc[17:26])
    return at


def universal_time(hh, mm, ss):
    ut = int(hh) + (int(mm) / 60.) + (float(ss) / 3600.)
    return ut


def julian_day(year, month, day, ut):

        # get B for Julian Day equation
        A = int(year / 100)
        B = 2 - A + int(A / 4)

        jd = int(365.25 * (year + 4716)) + \
        int(30.6001 * (month + 1)) + \
        day + ut/24.0 + \
        B - 1525.5
        return float(jd)


def jd_to_esd(jd):  # Earth-Sun distance (U.S. Naval Observatory)
    D = jd - 2451545.0
    g = 357.529 + 0.98560028 * D
    gr = math.radians(g)
    dES = 1.00014 - 0.01671 * math.cos(gr) - 0.00014 * math.cos(2 * gr)
    # check validity - maybe not necessary!
    if 0.983 <= dES <= 1.017:
        return dES
    else:
        msg = "The result is an invalid Earth-Sun distance. "
        "Please review input values!"
        raise ValueError(msg)


def utc_to_esd(utc): 
    at = extract_time_elements(utc)
    ut = universal_time(at['hours'], at['minutes'], at['seconds'])
    jd = julian_day(at['year'], at['month'], at['day'], ut)
    dES = jd_to_esd(jd)
    return dES


class AcquisitionTime:
    def __init__(self, utc):
        self.utc = utc
        self.at = extract_time_elements(self.utc)
        self.year = self.at['year']
        self.month = self.at['month']
        self.day = self.at['day']
        self.hours = self.at['hours']
        self.minutes = self.at['minutes']
        self.seconds = self.at['seconds']

        self.ut = universal_time(self.hours, self.minutes, self.seconds)
        self.jd = julian_day(self.year, self.month, self.day, self.ut)
        self.esd = utc_to_esd(self.utc)

    def __str__(self):
        return "Acquisition time (UTC format): " + self.utc

#    def __str__(self):
#        return "Acquisition time (UTC format): " + self.utc + '\n' + \
#        "Julian Day: " + str(self.jd) + '\n' + \
#        "Earth-Sun Distance: " + str(self.esd)


# Exemplifying
#utc = '2014_11_12T16:47:08.000000Z;'
#utc_to_esd(utc)
#utcstamp = utc_to_esd(utc) ; print "UTC Stamp: ", utcstamp
#print utc_to_esd('2014_11_12T16:47:08.000000Z;')


"""
...example, the QuickBird launch date of:
October 18, 2001 at 18:51:26 GMT corresponds to the
Julian Day 2452201.286.
"""
#utc_to_esd('2001_10_18T18:51:26.000000Z;')
#print "Conversion: ", utc_to_esd('2001_10_18T18:51:26.000000Z;')
