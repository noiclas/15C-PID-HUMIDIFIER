This is a brief overview on how this system on the pi that interacts with the humidifier and the sensors works. If all works perfectly one doesn't need to know any of this to actually run the code, but when something inevitably goes wrong it's pretty essential to know.

getFourSensorData.py manages the four sensors that we had hooked up to the pi. If you have a different sensor configuration, you will doubtless need to edit this file to make it work. It runs on its own clock, based on the sensorParameters.pickle file which is given to it from your computer by sensorManager.py. It uses the file sensorArray.py to actually interact with the sensors. It saves sensorData.pickle on the pi in the 'experimentName folder'

PIDWithPlot.py ultimately controls the level to which the humidifier is set to, from 0 to 100. To do this, it requires levelParameters.pickle which is from the levelManager.py file on your computer. Once it initializes, it periodically unloads these parameters, unloads the sensor data, makes a decision based on that data and the parameters, and uses motorclass.py to set the power of the humidifier. It then pickles this decision to levelData.pickle.



