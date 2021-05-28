'''
Meant to run on the raspberry pi, given stimulus from sensorManager.py on computer
'''

import os
import time
import pickle
from motorclass import motor

def on():
    os.system('sudo /var/www/rfoutlet/codesend 4216115')

def off():
    os.system('sudo /var/www/rfoutlet/codesend 4216124')
    
    
def bangbangOneSensor(PIDParameters,sensorData):
    goal = PIDParameters['goal']
    if sensorData['values'][0][-1] > goal:
        value = 0
        off()
    if sensorData['values'][0][-1] <= goal:
        value=1
        on()
    return value

def danielPID(PIDParameters, sensorData, whichSensor = 1):
    try:
        P = PIDParameters['P']
        I = PIDParameters['I']
    except:
        P = 10
        I = 50
    pError = sensorData['values'][whichSensor -1][-1] - PIDParameters['targetHumidity']
    iError = 0 #Make this work
    totalError = P * pError + I * iError
    power = 55 - totalError
    if (power > 100):
        power = 100
    elif (power < 0):
        power = 0
    global m
    m.setPower(power)
    return power

def levelTask(experimentName,PIDParameters,function = danielPID):
    #pull sensor data
    try:
        pOff = open('/home/pi/Documents/{}/sensorData.pickle'.format(experimentName),'rb')
        sensorData = pickle.load(pOff)
    except:
        time.sleep(0.02)
        pOff = open('/home/pi/Documents/{}/sensorData.pickle'.format(experimentName),'rb')
        sensorData = pickle.load(pOff)
    try:
        #pull previous level data and append
        pOff = open('/home/pi/Documents/{}/levelData.pickle'.format(experimentName),'rb')
        levelData = pickle.load(pOff)
        deltaT = time.time() - levelData['initialTime']
        value = function(PIDParameters,sensorData)
        levelData['times'].append(deltaT)
        levelData['values'].append(value)
    except Exception as e:
        print(e)
        #initialize levelData
        initialTime = time.time()
        value = function(PIDParameters,sensorData)
        levelData = {'times':[0],'values':[value],'initialTime':initialTime}
    pOn = open('/home/pi/Documents/{}/levelData.pickle'.format(experimentName),'wb')
    pickle.dump(levelData,pOn)
    pOn.close()
    
        

def manageTask():
    while True:
        startOfIteration = time.time()
        
        pickle_off = open('/home/pi/Documents/levelParameters.pickle','rb')
        parameters = pickle.load(pickle_off)
        
        if parameters['running']==False:
            off()
            os.system('rm /home/pi/Documents/levelParameters.pickle')
            break
        
        levelTask(experimentName=parameters['experimentName'],PIDParameters=parameters['PIDParameters'])
        
        elapsedTime = time.time()-startOfIteration
        period= parameters['period']
        if elapsedTime < period:
            time.sleep(period - elapsedTime)
        else:
            print('Could not control timing. Elapsed time: {}'.format(elapsedTime))

m = motor()
m.initializePower()
m.outletOn(True)
manageTask()
