import sys, os
sys.path.insert(0, os.path.abspath('..'))

import threading
from multiprocessing import Queue

from functools import partial


print = partial(print, flush=True)


class PibbleMotor:
    def __init__(self):
        print("inited Motor")

    
    def commandMove(self, args):
        return None

    def commandStop(self):
        return None