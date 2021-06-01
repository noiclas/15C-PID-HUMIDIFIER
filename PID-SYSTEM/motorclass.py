import RPistepper as stp
import os

class motor:
    
    def __init__(self):
        self.M1_pins = [22, 10, 9, 11]
        self.degreeRange = 150
        self.currentSetting = 100
        self.isOutletOn = False
        
    def stepDegrees(self, degrees):
        steps = int((degrees / 360) * 3096)
        with stp.Motor(self.M1_pins) as M1:
            M1.DELAY = 0.0015
            M1.move(steps)#One rotation is 3096

    def initializePower(self):
        with stp.Motor(self.M1_pins) as M1:
            M1.DELAY = 0.0015
            M1.move(2580)
        self.currentSetting = 100

    def setPower(self, powerLevel):
        deltaP = powerLevel - self.currentSetting
        deltaDegrees = self.degreeRange * deltaP / 100
        self.currentSetting = powerLevel
        if (powerLevel == 0):
            self.outletOn(False)
        else:
            self.outletOn(True)
        self.stepDegrees(deltaDegrees)

    def outletOn(self, setting):
        if (setting == True):
            os.system("sudo /var/www/rfoutlet/codesend 4216115")
            self.isOutletOn = True
        else:
            os.system("sudo /var/www/rfoutlet/codesend 4216124")
            self.isOutletOn = False
