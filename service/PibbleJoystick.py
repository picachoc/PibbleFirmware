import math

from functools import partial


print = partial(print, flush=True)

class PibbleJoystick():
    def __init__(self, brain, motor):
        self.brain = brain
        self.motor = motor
        self.inited = False

    def init(self):
        if not (self.brain.inited and self.motor.inited):
            self.inited = False
            return False
        else:
            try:
                self.inited = True
                return True
            except(Exception) as err:
                print(err)
                self.inited = False
                return {"error" : str(err)}


    def json(self, data):
        if data["phase"] == "move":
            force_x = data["force"] * math.cos(data["angle"]*math.pi/180.0)
            force_y = data["force"] * math.sin(data["angle"]*math.pi/180.0)

            self.motor.commandMove(force_x, force_y)
