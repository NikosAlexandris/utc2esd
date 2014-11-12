# -*- coding: utf-8 -*-
"""
@author: Nikos Alexandris| Created on Wed Nov 12 16:22:18 2014
"""


"""
Calculating Earth - Sun Distance

Aquisition Time ->  Julian Day

Source:
"""

import math


"""
The acquisition time in .IMD files, uses the UTC time format:
    YYYY_MM_DDThh:mm:ss:ddddddZ;
"""
utc = '2014_11_12T16:47:08.000000Z;'

#print "Year: ", utc[:4]
#print "Month: ", utc[5:7]
#print "Day: ", utc[8:10]
#print "Hours: ", utc[11:13]
#print "Minutes: ", utc[14:16]
#print "Seconds: ", utc[17:26] + utc[26]
#print

# helper functions ----------------------------------------------------------
# calculate Julian Day
def jd(year, month, day, ut, B):
        jd = int(365.25 * (year + 4716)) + \
        int(30.6001 * (month + 1)) + \
        day + ut/24.0 + \
        B - 1525.5
        return jd

# extract Year, Month, Day, Hours, Minutes, Seconds from UTC string
def utc_to_jd(utc):
    year = int(utc[:4])
    month = int(utc[5:7])
    day = int(utc[8:10])
    hh = int(utc[11:13])
    mm = int(utc[14:16])
    ss = float(utc[17:26])
    
    # Universal Time
    ut = hh + ( mm / 60. ) + ( ss /3600. )
    print "Universal Time: ", ut
    
    # Modify for Jan, Feb
    if month == 'January' or month == 'February':
        year -= 1
        month += 12
    
    # get B for Julian Day equation
    A = int(year / 100)
    B = 2 - A + int(A / 4)

    jd = jd(year, month, day, ut, B)
    print "Julian Day: ", jd
    
    # Earth-Sun distance (U.S. Naval Observatory)
    D = jd - 2451545.0
#    print "D: ", D
    
    g = 357.529 + 0.98560028 * D
    gr = math.radians(g)
    dES = 1.00014 - 0.01671 * math.cos(gr) - 0.00014 * math.cos(2 * gr)
    if 0.983 <= dES <= 1.017:
        print "Earh-Sun distance (dES) in Astronomical Units (AU): ", dES
    else:
        msg = "The result is an invalid Earth-Sun distance. "
        "Please review input values!"
        raise ValueError(msg)

utc_to_jd('2014_11_12T16:47:08.000000Z;')