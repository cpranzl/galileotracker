#!/usr/bin/env python

__author__ = "Christoph Pranzl"
__copyright__ = "Copyright 2016, Christoph Pranzl"
__credits__ = ["Christoph Pranzl"]
__license__ = "GPL-2.0"
__version__ = "0.0.1"
__maintainer__ = "Christoph Pranzl"
__email__ = "christoph.pranzl@fasolt.net"
__status__ = "prototype"

"""
SYNOPSIS

    galileotracker [-c,--coordinates] [-e,--elevation] [-t,--time]
                   [-h,--help] [-a,--apparent] [-v,--verbose] [--version]

DESCRIPTION

    galileotracker receives a textfile with the orbital elements of
    the galileo global navigation satellite system. The textfile contains
    this information as Two-Line-Element sets. Then it calculates
    altitude and azimuth of the satellite regarding a given location
    and time.

    If no coordinates are provided then Traun will be set as observers position

    If no point in time is provided actual time is used

    If --apparent is used only visible satellites are outputed

EXAMPLES

    galileotracker

    No parameters age given, altitude and azimuth are calculated for an observer in
    Traun right now

    galileotracker --coordinates=14.221162,48.223560 --elevation=273 --time=2016-06-23T10:00:00

    Coordinates as well as elevation and a time is provided. Altitude and elevation
    are calculated for the given moment in time.


EXIT STATUS

    TODO: List exit codes

"""

import sys, os, traceback, optparse
import re
import math
import time
from datetime import datetime
import ephem
import urllib2
import dateutil.parser

def main():

    global options, args

    if options.verbose: print("Coordinates: " + options.coordinates)
    if options.verbose: print("Elevation (m): " + str(options.elevation))
    if options.verbose: print("Time: " + str(options.time))

    coordinates = options.coordinates.split(",")
    degrees_per_radian = 180.0 / math.pi

    home = ephem.Observer()
    home.lon = coordinates[0]
    home.lat = coordinates[1]
    home.elevation = options.elevation
    home.date = dateutil.parser.parse(options.time)

    tle = []
    response = urllib2.urlopen(options.url)
    text = response.read()
    list = text.split('\n')
    del list[-1]
    for line in list:
        start = line[0]
        if start == '2':
        tle.append(line.strip(' \t\n\r'))
        gsat = ephem.readtle(tle[0],tle[1],tle[2])
        gsat.compute(home)
        info = home.next_pass(gsat)
        rise_time = dateutil.parser.parse(str(info[0]))
        set_time = dateutil.parser.parse(str(info[4]))
        if options.apparent:
            if gsat.alt > 0:
            print(str(tle[0]) + ', altitude % 4.1f deg, azimuth % 5.1f deg' % (gsat.alt * degrees_per_radian, gsat.$
                if options.verbose: print('Rise time: ' + str(rise_time))
                if options.verbose: print(' Set time: ' + str(set_time))
            else:
            print(str(tle[0]) + ', altitude %4.1f deg, azimuth %5.1f deg' % (gsat.alt * degrees_per_radian, gsat.az$
            if options.verbose: print('Rise time: ' + str(rise_time))
            if options.verbose: print(' Set time: ' + str(set_time))
        tle = []
        else:
        tle.append(line.strip(' \t\n\r'))

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], versio$
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        parser.add_option ('-c', '--coordinates', dest='coordinates', default='14.221162,48.223560', type='string',$
    parser.add_option ('-e', '--elevation', dest='elevation', default='273', type='int', help='Elevation of the obs$
        parser.add_option ('-t', '--time', dest='time', default=str(datetime.utcnow().isoformat()), type='string', $
    parser.add_option ('-a', '--apparent', action='store_true', default=False, help='Show only apparent satellites')
    parser.add_option ('-u', '--url', dest='url', default='https://www.celestrak.com/NORAD/elements/galileo.txt', t$
    (options, args) = parser.parse_args()
        if options.verbose: print(datetime.utcnow().isoformat())
        main()
        if options.verbose: print(datetime.utcnow().isoformat())
        if options.verbose: print 'TOTAL CALCULATION TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
