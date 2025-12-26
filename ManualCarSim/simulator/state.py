class CarState:
    def __init__(self):
        self.engine_on = True
        self.gear = 0
        self.speed = 0.0
        self.rpm = 800

    def reset(self):
        self.engine_on = True
        self.gear = 0
        self.speed = 0.0
        self.rpm = 800
