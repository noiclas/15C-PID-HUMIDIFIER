import os
from datetime import datetime
import time


import paramiko
ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.50.129',username='pi',password='raspberry')
ftp_client=ssh_client.open_sftp()


experimentName = None
if experimentName == None:
    experimentName = 'xpTwo'
os.system('mkdir {}'.format(experimentName))
ssh_client.exec_command('mkdir /home/pi/Documents/{}'.format(experimentName))

import plotManager
plotManager = plotManager.plotManager(experimentName = experimentName)
import sensorManager
sensorManager = sensorManager.sensorManager(experimentName = experimentName)
import levelManager
levelManager = levelManager.levelManager(experimentName = experimentName)

'''
To operate the pipeline:
    
First, make sure all the three managers plus the plotting tool are downloaded to the current working directory of this file

Make sure your experiment name is what you want it to be.

Then, get the sensor started. The command for this is sensorManager.start(period=0.5) (the default is 0.5). ssh into the pi
    and do an ls on the folder of the experimentName. If sensorData.pickle is there, that probably means the sensor is working.
    If sensorData.pickle is not there, there's probably some error with the I2C connection. Restart the pi, delete the folders if you want
    run the pipeline again, and try again until it works.

Next, get the levelManager started. The command is levelManager.start(period=1,PIDParameters). The PIDParameters are whatever you want to give 
    to your algorithm, which can be defined in the PIDWithPlot.py file on the pi. For example, you could let PIDParameters = {'goal':80}, 
    if your algorithm takes in a goal humidity argument. Period is just how often it'll run.
    
Finally, get plotManager started. Command is plotManager.start(period=1). For weird reasons with the timing of it pulling pickles from the pi,
it'll sometimes fail. It's not too bad to fix, just import and define another plotManager and start it again.

To update arguments: You can call sensorManager.update(running,period), the defaults are whatever they were before. To stop the sensor, do
    sensorManager.update(running=False). Same for levelManager, but do levelManager.update(running,period,PIDParameters). To stop the plotter, do
    plotManager.stop()


'''






