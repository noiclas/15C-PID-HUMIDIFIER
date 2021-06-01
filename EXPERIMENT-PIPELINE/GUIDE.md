This is a guide on how to run the humidifier and manage data from one's computer 

ESSENTIAL STEPS TO SET UP EXPERIMENT

1) Get the raspberry pi and humidifier all wired up as described in this repo, with the files from PID-SYSTEM downloaded on the raspberry pi in the /home/pi/Documents folder.

2) Download all of the .py files in this directory to one single folder on your computer. You'll need to go through each file and change the ip address to that of your raspberry pi.

ESSENTIAL STEPS TO RUN EXPERIMENT

1) Open piControl.py in spyder Python 3.8 (it may work in other editors but this is the only one it has been tested in). Change the experimentName variable to something unique, then run it. This initializes three management objects that you use to talk to the raspberry pi and plot data, and creates the 'experimentName' folder that the computer and the pi will use to talk to eachother.

2) Start the humidity sensors, with sensorManager.start(period=0.5). You can also just call sensorManager.start(). Check the 'experimentName' folder on the pi. You should see sensorData.pickle there. If you don't, it's not working. Restart the pi and try again, or you could debug more by calling getFourSensorData.py on the raspberry pi itself.

3) Start the PID algorithm, with levelManager.start(initialize=True, period = 2, PIDParameters = {'targetHumidity':65,'P':6,'I':0.01,'integralTime':20,'setPoint':65}). This will give the PIDWithPlot.py file on the raspberry pi some parameters to work with, and tells it to start running. Again, verify that it is working by checking the 'experimentName' folder on the pi. You should see levelData.pickle there. If you don't, try debugging by running PIDWithPlot.py on the pi manually.

OPTIONAL STEPS DURING EXPERIMENT

Initialize the plotter, with plotManager.start(). You should see a live plot with the top plot the sensor readings over time, and the bottom plot the level setting over time.

Update any of the PID parameters with levelManager.update(PIDParameters = {'targetHumidity':65,'P':6,'I':0.01,'integralTime':20,'setPoint':65}) (or whatever values you want).

Stop the PID with levelManager.update(running=False). If at any point you need to restart the PID, run levelManager.start(initialize=False,period=2,PIDParameters = PIDParameters)

Stop the sensor with sensorManager.update(running=False).

Stop the plotter with plotManager.stop()



