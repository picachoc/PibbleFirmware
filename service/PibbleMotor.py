import sys, os
sys.path.insert(0, os.path.abspath('..'))

import time

import threading
from multiprocessing import Queue

from functools import partial


print = partial(print, flush=True)


class PibbleMotor:
    def __init__(self, brain):
        self.MAX_MICRO_STEP = 16
        self.MAX_SPEED = 100

        self.inited = False
        self.brain = brain

        self.running = False
        self.moving = False

        self.speed = 0

        self.step_count = {"alt" : 0, "az" : 0}         ## Step_count is counted with the smallest step possible, meaning that 1 step with micro_step = 1 will count as MAX_MICRO_STEP in step_count
        self.micro_stepping = self.MAX_MICRO_STEP
        self.last_step_filled = None

        self.instructions = Queue()
        self.movement_lock = threading.Lock()

        self.stepper = threading.Thread(target=self.steppingThread, daemon=True)


    def init(self):
        if not self.brain.inited:
            self.inited = False
            return False
        else:   
            try:
                self.stepper.start()
                self.running = True
                self.inited = True
                return True
            except(Exception) as err:
                print(err)
                self.running = False
                self.inited = False
                return {"error" : str(err)}


    def steppingThread(self):
        while self.running:
            self.movement_lock.acquire()
            if not self.instructions.empty() and self.moving:
                step_alt, step_az, speed = self.instructions.get()       ## Each instruction is a tuple like this : (alt, az, speed) where "alt" and "az" are integers between -1 and 1 and speed a float
                if step_alt < 0:
                    print("Step Alt down")
                elif step_alt > 0:
                    print("Step Alt up")
                if step_az < 0:
                    print("Step Az CCW")
                elif step_az > 0:
                    print("Step Az CW")

                self.step_count["alt"] += int(self.MAX_MICRO_STEP/self.micro_stepping) * step_alt
                self.step_count["az"] += int(self.MAX_MICRO_STEP/self.micro_stepping) * step_az
                
                time.sleep(speed/1000)
            self.movement_lock.release()
        return None


    def commandMove(self, args):
        return None

    def commandStop(self):
        return None

    def commandAbort(self):
        try:
            self.moving = False
            self.movement_lock.acquire()
            while not self.instructions.empty():
                self.instructions.get()
            self.speed = 0
            self.micro_stepping = self.MAX_MICRO_STEP
            self.last_step_filled = None
            self.movement_lock.release()
            return {"result" : "Movements aborted"}
        except(Exception) as err:
            print(err)
            return {"error" : str(err)}

    def __del__(self):
        self.running = False
