from functools import partial


print = partial(print, flush=True)

class PibbleJoystick():
    def __init__(self, brain):
        self.brain = brain
        self.inited = False

    def init(self):
        if not self.brain.inited:
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
        print(data)
