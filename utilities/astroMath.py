import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, ICRS

from datetime import datetime
import time

import numpy as np

def utcFromGeoloc(longitude=0, latitude=0, local_time=0):
    return None
    
def getAltAz(astropy_coords, astropy_location, telescope_time):
    return astropy_coords.transform_to(AltAz(location=astropy_location, obstime=telescope_time))
