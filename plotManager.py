import pickle
import time
import numpy as np
import subprocess
import matplotlib.pyplot as plt
import dynamicPlottingTool
from threading import Thread

import paramiko
ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.50.129',username='pi',password='raspberry')
ftp_client=ssh_client.open_sftp()

class plotManager():
    def __init__(self,dataFormat=0,experimentName=''):
        self.dataFormat = dataFormat
        self.experimentName = experimentName
    
    def oneSensor(self):
        global ftp_client
        try:
            ftp_client.get('/home/pi/Documents/{}/sensorData.pickle'.format(self.experimentName),'{}/sensorData.pickle'.format(self.experimentName))
        except:
            time.sleep(0.05)
            ftp_client.get('/home/pi/Documents/{}/sensorData.pickle'.format(self.experimentName),'{}/sensorData.pickle'.format(self.experimentName))
        pickleOff = open('{}/sensorData.pickle'.format(self.experimentName),'rb')
        sensorData = pickle.load(pickleOff)
        datasets = {0:[sensorData['times'],sensorData['values'][0]]}
        self.plotter.plot(datasets)
        
    def fourSensors(self):
        global ftp_client
        try:
            ftp_client.get('/home/pi/Documents/{}/sensorData.pickle'.format(self.experimentName),'{}/sensorData.pickle'.format(self.experimentName))
        except:
            time.sleep(0.05)
            ftp_client.get('/home/pi/Documents/{}/sensorData.pickle'.format(self.experimentName),'{}/sensorData.pickle'.format(self.experimentName))
        pickleOff = open('{}/sensorData.pickle'.format(self.experimentName),'rb')
        sensorData = pickle.load(pickleOff)
        datasets = {0:[sensorData['times'],sensorData['values'][0],sensorData['values'][1],sensorData['values'][2],sensorData['values'][3]]}
        self.plotter.plot(datasets)
            
    def oneSensorPlusLevel(self):
        global ftp_client
        try:
            ftp_client.get('/home/pi/Documents/{}/sensorData.pickle'.format(self.experimentName),'{}/sensorData.pickle'.format(self.experimentName))
            ftp_client.get('/home/pi/Documents/{}/levelData.pickle'.format(self.experimentName),'{}/levelData.pickle'.format(self.experimentName))
        except:
            time.sleep(0.05)
            ftp_client.get('/home/pi/Documents/{}/sensorData.pickle'.format(self.experimentName),'{}/sensorData.pickle'.format(self.experimentName))
            ftp_client.get('/home/pi/Documents/{}/levelData.pickle'.format(self.experimentName),'{}/levelData.pickle'.format(self.experimentName))
        pickleOff = open('{}/sensorData.pickle'.format(self.experimentName),'rb')
        sensorData = pickle.load(pickleOff)
        pickleOff = open('{}/levelData.pickle'.format(self.experimentName),'rb')
        levelData = pickle.load(pickleOff)
        datasets = {0:[sensorData['times'],sensorData['values'][0]],1:[levelData['times'],levelData['values']]}
        self.plotter.plot(datasets)
    
    def fourSensorsPlusLevel(self):
        global ftp_client
        try:
            ftp_client.get('/home/pi/Documents/{}/sensorData.pickle'.format(self.experimentName),'{}/sensorData.pickle'.format(self.experimentName))
            ftp_client.get('/home/pi/Documents/{}/levelData.pickle'.format(self.experimentName),'{}/levelData.pickle'.format(self.experimentName))
        except:
            time.sleep(0.05)
            ftp_client.get('/home/pi/Documents/{}/sensorData.pickle'.format(self.experimentName),'{}/sensorData.pickle'.format(self.experimentName))
            ftp_client.get('/home/pi/Documents/{}/levelData.pickle'.format(self.experimentName),'{}/levelData.pickle'.format(self.experimentName))
        pickleOff = open('{}/sensorData.pickle'.format(self.experimentName),'rb')
        sensorData = pickle.load(pickleOff)
        pickleOff = open('{}/levelData.pickle'.format(self.experimentName),'rb')
        levelData = pickle.load(pickleOff)
        datasets = {0:[sensorData['times'],sensorData['values'][0],sensorData['values'][1],sensorData['values'][2],sensorData['values'][3]],1:[levelData['times'],levelData['values']]}
        self.plotter.plot(datasets)
        
    
    def fourSensorsWithDump(self):
        global ftp_client
        try:
            ftp_client.get('/home/pi/Documents/dump.p','dump.pickle')
        except:
            time.sleep(0.69)
            ftp_client.get('/home/pi/Documents/dump.p','dump.pickle')
        pOff = open('dump.pickle','rb')
        dump = pickle.load(pOff)
        datasets = {0:[dump[0],dump[2][0],dump[2][1],dump[2][2],dump[2][3]]}
        self.plotter.plot(datasets)
        
    
    def updateParameter(self,index,name,value):
        self.plotter.dataFormat[index][name]=value
    
    def updateAll(self,name,value):
        for index in self.plotter.dataFormat:
            self.plotter.dataFormat[index][name]=value
        
    def runTask(self):
        self.running = True
        while self.running==True:
            startTime = time.time()
            
            try:
                self.fourSensorsPlusLevel()
            except:
                time.sleep(0.5)
                self.fourSensorsPlusLevel()
            
            elapsedTime = time.time()-startTime
            if elapsedTime >= self.period:
                print('Elapsed time for this iteration was {}'.format(elapsedTime))
            else:
                time.sleep(self.period-elapsedTime)
            
                
    def start(self,period=1):
        self.figure = plt.figure()
        self.plotter = dynamicPlottingTool.dynamicPlotter(self.figure,self.dataFormat)
        self.period = period
        t = Thread(target = self.runTask)
        t.start()
    
    def stop(self):
        self.running = False








            