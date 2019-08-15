from astropy.coordinates import AltAz

from datetime import datetime, timedelta


## time is a datetime object, and offset is an int in hours
def utcFromTimeZone(time, offset):
    return time - timedelta(hours=offset)


def getAltAz(astropy_coords, astropy_location, telescope_time):
    return astropy_coords.transform_to(AltAz(location=astropy_location, obstime=telescope_time))
