'''
Meant to run on the raspberry pi, given stimulus from levelManager.py on computer
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

def manualOverride(PIDParameters,sensorData):
    power = PIDParameters['power']
    global m
    m.setPower(power)
    return power

def danielPID(PIDParameters, sensorData, whichSensor = 1):
    try:
        P = PIDParameters['P']
        I = PIDParameters['I']
    except:
        P = 10
        I = 50
    pError = sensorData['values'][whichSensor -1][-1] - PIDParameters['targetHumidity']
    iError = getIError(PIDParameters,sensorData,whichSensor=1)
    totalError = P * pError + I * iError
    power = PIDParameters['setPoint'] - totalError
    if (power > 100):
        power = 100
    elif (power < 0):
        power = 0
    global m
    m.setPower(power)
    global diagnosticInfo
    diagnosticInfo['time'].append(sensorData['times'][-1])
    diagnosticInfo['iError'].append(iError)
    diagnosticInfo['pError'].append(pError)
    diagnosticInfo['totalError'].append(totalError)
    diagnosticInfo['humidity'].append(sensorData['values'][whichSensor-1][-1])
    diagnosticInfo['power'].append(power)
    global directory
    pickle.dump(diagnosticInfo,open(directory + "/diagnosticInfo.p","wb"))
    return power

def getIError(PIDParameters,sensorData,whichSensor=1,integralTime=100):
    integralTime = PIDParameters['integralTime']
    latestTime = sensorData['times'][-1]
    i=0
    while True:
        time = sensorData['times'][i]
        if latestTime - time < integralTime:
            firstIndex = i
            break
        i+=1
    lastIndex = len(sensorData['times'])-1
    s = 0
    for index in range(firstIndex,lastIndex+1):
        s += sensorData['values'][whichSensor-1][index] - PIDParameters['targetHumidity']
    iError = s / (lastIndex - firstIndex + 1) * integralTime
    print(firstIndex)
    print(iError)
    return iError

def levelTask(experimentName,PIDParameters,initialize,function = danielPID):
    #pull sensor data
    global directory
    directory = '/home/pi/Documents/{}'.format(experimentName)
    try:
        pOff = open('/home/pi/Documents/{}/sensorData.pickle'.format(experimentName),'rb')
        sensorData = pickle.load(pOff)
    except:
        time.sleep(0.2)
        pOff = open('/home/pi/Documents/{}/sensorData.pickle'.format(experimentName),'rb')
        sensorData = pickle.load(pOff)
    #load, or initialize, the previous levelData
    if initialize == True:
        initialTime = time.time()
        levelData = {'times':[],'values':[],'targetHumidity':[],'initialTime':initialTime}
    else:
        pOff = open('/home/pi/Documents/{}/levelData.pickle'.format(experimentName),'rb')
        levelData = pickle.load(pOff)
    #set value and append data
    deltaT = time.time() - levelData['initialTime']
    try:
        value = function(PIDParameters,sensorData)
    except:
        time.sleep(0.5)
        value = function(PIDParameters,sensorData)
    levelData['times'].append(deltaT)
    levelData['values'].append(value)
    levelData['targetHumidity'].append(PIDParameters['targetHumidity'])
    #pickle levelData.pickle pack
    pOn = open('/home/pi/Documents/{}/levelData.pickle'.format(experimentName),'wb')
    pickle.dump(levelData,pOn)
    pOn.close()
    
        

def manageTask():
    global initialize
    while True:
        startOfIteration = time.time()
        
        pickle_off = open('/home/pi/Documents/levelParameters.pickle','rb')
        parameters = pickle.load(pickle_off)
        
        if parameters['running']==False:
            off()
            os.system('rm /home/pi/Documents/levelParameters.pickle')
            break
        
        levelTask(experimentName=parameters['experimentName'],PIDParameters=parameters['PIDParameters'],initialize=initialize)
        initialize=False
        
        elapsedTime = time.time()-startOfIteration
        period= parameters['period']
        if elapsedTime < period:
            time.sleep(period - elapsedTime)
        else:
            print('Could not control timing. Elapsed time: {}'.format(elapsedTime))

pickle_off = open('/home/pi/Documents/levelParameters.pickle','rb')
parameters = pickle.load(pickle_off)
initialize = parameters['initialize']


diagnosticInfo = {'iError':[],'pError':[],'totalError':[],'power':[],'humidity':[],'time':[]}
m = motor()
m.initializePower()
m.outletOn(True)
manageTask()
