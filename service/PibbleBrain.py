import sys, os
sys.path.insert(0, os.path.abspath('..'))

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, ICRS

from datetime import datetime
import time

import numpy as np

import threading
from multiprocessing import Queue

from utilities.astroMath import *


class PibbleBrain:
    def __init__(self):
        self.inited = False
        
        self.telescope_coords = {"longitude" : -0.000500, "latitude" : 51.476852}
        self.times = {"telescope_start_time" : datetime.utcnow(), "system_start_time" : datetime.utcnow(), "delta_time" : 0}
        ##self.telescope_position = {""}

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
        return datetime.utcnow() - self.times["delta_time"]

    def createCoords(self, obj, q=None):
        obj.update({"astropy_coords" : SkyCoord("05 55 09 +07 24 28.3", unit=(u.hourangle, u.deg))})
        if q:
            q.put(obj)
        return None

    def getVisibles(self, obj_list):
        visible_list = []
        coords_list = []
        threads = []
        q = Queue()
        
        number = len(obj_list)
        for x in range(0, number):
            threads[x].append(threading.Thread(target=createCoords, args=(self, obj_list[x], q), daemon=True))
            threads[x].start()

        nb = 0
        while nb != number:
            while not q.empty():
                obj = q.get()
                coords_list.append(getAltAz(obj["astropy_coords"], self.astropy_location, self.getTime()))
                nb += 1
                
            while len(coords_list) != 0:
                star = coords_list.pop(0)
                if star["astropy_altaz"].alt.degree > 0:
                    star.pop("astropy_altaz")
                    star.pop("astropy_coords")
                    visible_list.append(star)

        return visible_list
