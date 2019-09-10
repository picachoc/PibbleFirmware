import sys, os
sys.path.insert(0, os.path.abspath('..'))

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, solar_system_ephemeris

from functools import partial
from datetime import datetime
import time

import numpy as np

import threading
from multiprocessing import Queue

from utilities.astroMath import getAltAz
from utilities.astroMath import utcFromTimeZone


print = partial(print, flush=True)


class PibbleBrain:
    def __init__(self):
        self.MAX_THREAD_COUNT = 100

        self.inited = False

        self.telescope_coords = {"longitude" : -0.000500, "latitude" : 51.476852}
        self.times = {"telescope_start_time" : datetime.utcnow(), "system_start_time" : datetime.utcnow(), "delta_time" : 0}        ## All times are utc
        self.telescope_position = {"alt" : 0, "az" : 0, "ra" : 0, "dec" : 0}

        self.astropy_location = None
        self.astropy_coords = {}

        solar_system_ephemeris.set("de430")

    def init(self, args):
        try:
            self.telescope_coords["latitude"] = float(args["latitude"])
            self.telescope_coords["longitude"] = float(args["longitude"])

            self.times["telescope_start_time"] = utcFromTimeZone(datetime.fromtimestamp(float(args["timestamp"])/1000.0), int(args["offset"]))
            self.times["system_start_time"] = datetime.utcnow()
            self.times["delta_time"] = self.times["telescope_start_time"] - self.times["system_start_time"]

            self.astropy_location = EarthLocation(lat=np.array(self.telescope_coords["latitude"])*u.deg,lon=np.array(self.telescope_coords["longitude"])*u.deg)
            self.inited = True
        except(Exception) as err:
            self.inited = False
            print(err)
            return {"error" : str(err)}

    def getTime(self):
        return datetime.utcnow() - self.times["delta_time"] ##returns the utc time synced with the phone, that way, it is right even if the pi hasn't the good one.

    def createCoords(self, obj, q=None, semaphore=None):
        try:
            obj.update({"astropy_coords" : SkyCoord(ra=obj["ra"], dec=obj["declination"], unit=(u.hourangle, u.deg))})
            if q:
                q.put(obj)
            if semaphore:
                semaphore.release()
            return obj
        except(Exception) as err:
            print(err)
            return None

    def getVisibles(self, obj_list):
        try:
            star = obj_list.copy() ## prevent obj_list from being modified
            visible_list = []
            threads = []
            q = Queue()
            current_time = self.getTime()

            sema = threading.Semaphore(self.MAX_THREAD_COUNT)       ## Prevents from running more than self.MAX_THREAD_COUNT threads at once.

            number = len(star)
            for x in range(0, number):
                """while len(threads) >= 100:
                    size = len(threads)
                    for x in range(0, size):
                        if not threads[x].is_alive:
                            threads.pop(x)
                            x = 0
                            size = len(threads)"""

                sema.acquire()      ## Blocks while more than 100 threads are running at once.
                threads.append(threading.Thread(target=self.createCoords, args=(star[x], q, sema), daemon=True))
                threads[len(threads)-1].start()

            nb = 0
            while nb < number:
                while not q.empty():
                    obj = q.get()
                    angle = getAltAz(obj["astropy_coords"], self.astropy_location, current_time).alt.degree
                    if  angle > 0 and angle < 180:
                        obj.pop("astropy_coords")
                        visible_list.append(obj)
                    nb += 1
            return visible_list
        except(Exception) as err:
            print(err)
            return {"error" : str(err)}

    def getAllEphemerides(self):
        try:
            ephemerides = solar_system_ephemeris.bodies
            
            return ephemerides
        except(Exception) as err:
            print(err)
            return {"error" : str(err)}

    def returnPositions(self):
        return self.telescope_position
        