import sys, os
sys.path.insert(0, os.path.abspath('..'))

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation

from functools import partial
from datetime import datetime
import time

import numpy as np

import threading
from multiprocessing import Queue

from utilities.astroMath import getAltAz


print = partial(print, flush=True)


class PibbleBrain:
    def __init__(self):
        self.inited = False
        
        self.telescope_coords = {"longitude" : -0.000500, "latitude" : 51.476852}
        self.times = {"telescope_start_time" : datetime.utcnow(), "system_start_time" : datetime.utcnow(), "delta_time" : 0}        ## All times are utc
        self.telescope_position = {"alt" : 0, "az" : 0, "ra" : 0, "dec" : 0}

        self.astropy_location = None
        self.astropy_coords = {}

    def init(self):
        try:
            self.astropy_location = EarthLocation(lat=np.array(self.telescope_coords["latitude"])*u.deg,lon=np.array(self.telescope_coords["longitude"])*u.deg)
            self.inited = True
        except(Exception) as err:
            self.inited = False
            print(err, flush=True)
            return None

    def getTime(self):
        return datetime.utcnow() - self.times["delta_time"] ##returns the utc time synced with the phone, that way, it is right even if the pi hasn't the good one.

    def createCoords(self, obj, q=None):
        obj.update({"astropy_coords" : SkyCoord(ra=obj["ra"], dec=obj["declination"], unit=(u.hourangle, u.deg))})
        if q:
            q.put(obj)
        return obj

    def getVisibles(self, obj_list):
        star = obj_list.copy() ## prevent obj_list from being modified
        visible_list = []
        threads = []
        q = Queue()
        current_time = self.getTime()
        
        number = len(star)
        for x in range(0, number):
            threads[x].append(threading.Thread(target=createCoords, args=(self, star[x], q), daemon=True))
            threads[x].start()

        nb = 0
        while nb != number:
            while not q.empty():
                obj = q.get()
                if getAltAz(obj["astropy_coords"], self.astropy_location, current_time).alt.degree > 0:
                    star.pop("astropy_coords")
                    visible_list.append(star)
                nb += 1

        return visible_list

    def returnPositions(self):
        return self.telescope_position