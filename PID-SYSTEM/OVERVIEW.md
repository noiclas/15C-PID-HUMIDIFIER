This is a brief overview on how this system on the pi that interacts with the humidifier and the sensors works. If all works perfectly one doesn't need to know any of this to actually run the code, but when something inevitably goes wrong it's pretty essential.

getFourSensorData.py manages the four sensors that we had hooked up to the pi. If you have a different sensor configuration, you will doubtless need to edit this file to make it work. It runs on its own clock, based on the sensorParameters.pickle file which is given to it from your computer by sensorManager.py. 



