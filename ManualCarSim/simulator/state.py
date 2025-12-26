class CarState:
    def __init__(self):
        self.engine_on = True
        self. gear = 0
        self. speed = 0.0
        self.rpm = 800
        self.handbrake = False
        self.on_hill = False
    
    def reset(self):
        self.engine_on = True
        self.gear = 0
        self.speed = 0.0
        self.rpm = 800
        self.handbrake = False
        # Keep hill setting as is
    
    def stall(self):
        self.engine_on = False
        self.rpm = 0