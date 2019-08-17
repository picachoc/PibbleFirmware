import sys, os
sys.path.insert(0, os.path.abspath('..'))

import threading
from multiprocessing import Queue

from functools import partial


print = partial(print, flush=True)


class PibbleMotor:
    def __init__(self, brain):
        self.inited = False
        self.brain = brain

        self.running = False
        self.moving = False

        self.max_speed = 100
        self.speed = 0

        self.instructions = Queue()
        self.instructions_lock = threading.Lock()

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
            self.instructions_lock.acquire()
            if not self.instructions.empty() and self.moving:
                step = self.instructions.get()       ## Each instruction is a tuple like this : (alt, az) where "alt" and "az" are integers and can have negative values
            self.instructions_lock.release()
        return None


    def commandMove(self, args):
        return None

    def commandStop(self):
        self.moving = False
        self.instructions_lock.acquire()
        while not self.instructions.empty():
            self.instructions.get()
        self.instructions_lock.release()
        return None
        