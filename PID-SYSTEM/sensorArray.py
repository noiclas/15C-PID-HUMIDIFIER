import board
import busio
from adafruit_htu21d import HTU21D
from adafruit_tca9548a import TCA9548A
import time
import numpy as np
import pickle

class sensorArray:

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.tca = TCA9548A(self.i2c)
        self.sensor1 = HTU21D(self.tca[2])
        self.sensor2 = HTU21D(self.tca[4])
        self.sensor3 = HTU21D(self.tca[6])
        self.sensor4 = HTU21D(self.tca[7])

        self.loadCalibration()

    def calibrate(self, maxTime = 5):
        startTime = time.time()
        deltaTime = time.time() - startTime
        
        humidities1 = []
        humidities2 = []
        humidities3 = []
        humidities4 = []
        
        while (deltaTime <= maxTime):
            humidities1.append(self.sensor1.relative_humidity)
            humidities2.append(self.sensor2.relative_humidity)
            humidities3.append(self.sensor3.relative_humidity)
            humidities4.append(self.sensor4.relative_humidity)
            deltaTime = time.time() - startTime

        avg1 = np.average(humidities1)
        avg2 = np.average(humidities2)
        avg3 = np.average(humidities3)
        avg4 = np.average(humidities4)
        totalAvg = np.average([avg1,avg2,avg3,avg4])

        delta1 = avg1 - totalAvg
        delta2 = avg2 - totalAvg
        delta3 = avg3 - totalAvg
        delta4 = avg4 - totalAvg

        dumpFile = [delta1, delta2, delta3, delta4]
        pickle.dump(dumpFile, open("calibration.p","wb"))
        self.loadCalibration()

    def loadCalibration(self):
        calibrationFile = pickle.load(open("/home/pi/Documents/calibration.p","rb"))
        self.delta1 = calibrationFile[0]
        self.delta2 = calibrationFile[1]
        self.delta3 = calibrationFile[2]
        self.delta4 = calibrationFile[3]

        print("Loaded calibration" + str(calibrationFile))
                    
    def getHumidity(self, id, rawData = False):
        if (rawData):
            if (id == 1):
                return self.sensor1.relative_humidity
            elif (id == 2):
                return self.sensor2.relative_humidity
            elif (id == 3):
                return self.sensor3.relative_humidity
            elif (id == 4):
                return self.sensor4.relative_humidity
        else:
            if (id == 1):
                return self.sensor1.relative_humidity - self.delta1
            elif (id == 2):
                return self.sensor2.relative_humidity - self.delta2
            elif (id == 3):
                return self.sensor3.relative_humidity - self.delta3
            elif (id == 4):
                return self.sensor4.relative_humidity - self.delta4

    def getTemperature(self, id):
        if (id == 1):
            return self.sensor1.temperature
        elif (id == 2):
            return self.sensor2.temperature
        elif (id == 3):
            return self.sensor3.temperature
        elif (id == 4):
            return self.sensor4.temperature
    
