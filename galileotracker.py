#!/usr/bin/env python3

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

    No parameters age given, altitude and azimuth are calculated for an
    observer in Traun right now

    galileotracker --coordinates=14.221162,48.223560 --elevation=273
                   --time=2016-06-23T10:00:00

    Coordinates as well as elevation and a time is provided. Altitude and
    elevation are calculated for the given moment in time.

"""

import sys, os, traceback, argparse
import re
import math
import time
from datetime import datetime
import ephem
from urllib.request import urlopen
import dateutil.parser


def main():

    global args

    if args.verbose: print("Coordinates: " + args.coordinates)
    if args.verbose: print("Elevation (m): " + str(args.elevation))
    if args.verbose: print("Time: " + str(args.time))

    coordinates = args.coordinates.split(",")
    degrees_per_radian = 180.0 / math.pi

    home = ephem.Observer()
    home.lon = coordinates[0]
    home.lat = coordinates[1]
    home.elevation = args.elevation
    home.date = dateutil.parser.parse(args.time)

    tle = []
    prefix = '2'

    with urlopen(args.url) as response:
        for line in response:
            line = line.decode('utf-8')
            start = line[0]
            if start == prefix:
                tle.append(line.strip('\r\n'))
                gsat = ephem.readtle(tle[0],tle[1],tle[2])
                gsat.compute(home)
                info = home.next_pass(gsat)
                rise_time = dateutil.parser.parse(str(info[0]))
                set_time = dateutil.parser.parse(str(info[4]))
                if args.apparent:
                    if gsat.alt > 0:
                        print("{0}, altitude {1:4.1f} deg, azimuth {2:5.1f} deg"\
                              .format(str(tle[0]), \
                                      gsat.alt * degrees_per_radian, \
                                      gsat.az * degrees_per_radian))
                        if args.verbose: print("Rise time: " + str(rise_time))
                        if args.verbose: print(" Set time: " + str(set_time))
                else:
                    print("{0}, altitude {1:4.1f} deg, azimuth {2:5.1f} deg"\
                              .format(str(tle[0]), \
                                      gsat.alt * degrees_per_radian, \
                                      gsat.az * degrees_per_radian))
                    if args.verbose: print("Rise time: " + str(rise_time))
                    if args.verbose: print(" Set time: " + str(set_time))
                tle = []
            else:
                tle.append(line.strip(' \r\n'))

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser =  argparse.ArgumentParser()
        parser.add_argument("-v", \
                            "--verbose", \
                            action="store_true", \
                            default=False, \
                            help="increase verbose output")
        parser.add_argument("-c", \
                            "--coordinates", \
                            default="14.221162,48.223560", \
                            help="Location of the observer")
        parser.add_argument("-e", \
                            "--elevation", \
                            dest="elevation", \
                            default=273, \
                            type=int, \
                            help="Elevation of the observer")
        parser.add_argument("-t", \
                            "--time", \
                            dest="time", \
                            default=str(datetime.utcnow().isoformat()), \
                            help="Point of time for calculation")
        parser.add_argument("-a", \
                            "--apparent", \
                            action="store_true", \
                            default=False, \
                            help="Show only apparent satellites")
        parser.add_argument("-u", \
                            "--url", \
                            dest="url", \
                            default="https://www.celestrak.com/NORAD/elements/galileo.txt", \
                            help="3")
        args = parser.parse_args()
        if args.verbose: print(datetime.utcnow().isoformat())
        main()
        if args.verbose: print(datetime.utcnow().isoformat())
        if args.verbose: print("TOTAL CALCULATION TIME IN MINUTES:")
        if args.verbose: print((time.time() - start_time) / 60.0)
        sys.exit(0)
    except KeyboardInterrupt as e:
        raise e
    except SystemExit as e:
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

