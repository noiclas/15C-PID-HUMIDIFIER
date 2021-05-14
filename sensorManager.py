import pickle

import paramiko
ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.50.129',username='pi',password='raspberry')
ftp_client=ssh_client.open_sftp()

class sensorManager():
    def __init__(self,experimentName=''):
        self.experimentName = experimentName
    
    def start(self,period=0.5):
        global ftp_client
        global ssh_client
        self.period = period
        self.running=True
        parameters = {'running':True,'period':period,'experimentName':self.experimentName}
        pickling_on = open('{}/sensorParameters.pickle'.format(self.experimentName),'wb')
        pickle.dump(parameters,pickling_on)
        pickling_on.close()
        ftp_client.put('{}/sensorParameters.pickle'.format(self.experimentName),'/home/pi/Documents/sensorParameters.pickle')
        ssh_client.exec_command('python3 /home/pi/Documents/getFourSensorData.py')
        
    def update(self,running=None,period=None):
        global ftp_client
        if running==None:
            running=self.running
        if period==None:
            period = self.period
        self.period = period
        self.running=running
        parameters = {'running':running,'period':period,'experimentName':self.experimentName}
        pickling_on = open('{}/sensorParameters.pickle'.format(self.experimentName),'wb')
        pickle.dump(parameters,pickling_on)
        pickling_on.close()
        ftp_client.put('{}/sensorParameters.pickle'.format(self.experimentName),'/home/pi/Documents/sensorParameters.pickle')
        
        
