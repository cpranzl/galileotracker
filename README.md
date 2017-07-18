# galileotracker

## SYNOPSIS
    galileotracker [-c,--coordinates] [-e,--elevation] [-t,--time] [-h,--help] [-a,--apparent] [-v,--verbose] [--version]

## DESCRIPTION
galileotracker receives a textfile with the orbital elements of the galileo global navigation satellite system. The textfile contains this information as Two-Line-Element sets. Then it calculates altitude and azimuth of the satellite regarding a given location and time.

* If no coordinates are provided then Traun will be set as observers position
* If no point in time is provided actual time is used
* If --apparent is used only visible satellites are outputed

## EXAMPLES
    galileotracker

No parameters age given, altitude and azimuth are calculated for an observer in Traun, Austria right now

    galileotracker --coordinates=14.221162,48.223560 --elevation=273 --time=2016-06-23T10:00:00

Coordinates as well as elevation and a time is provided. Altitude and elevation are calculated for the given moment in time.

## EXIT STATUS
TODO: List exit codes
