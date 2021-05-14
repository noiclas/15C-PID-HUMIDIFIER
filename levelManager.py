import pickle

import paramiko
ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.50.129',username='pi',password='raspberry')
ftp_client=ssh_client.open_sftp()

class levelManager():
    def __init__(self,experimentName):
        self.experimentName = experimentName
    
    def start(self,PIDParameters,period=1):
        global ftp_client
        global ssh_client
        self.period = period
        self.PIDParameters = PIDParameters
        self.running=True
        parameters = {'running':True,'period':period,'PIDParameters':PIDParameters,'experimentName':self.experimentName}
        pickling_on = open('{}/levelParameters.pickle'.format(self.experimentName),'wb')
        pickle.dump(parameters,pickling_on)
        pickling_on.close()
        ftp_client.put('{}/levelParameters.pickle'.format(self.experimentName),'/home/pi/Documents/levelParameters.pickle')
        ssh_client.exec_command('python3 Documents/PIDWithPlot.py')
        
    def update(self,running=None,period=None,PIDParameters=None):
        global ftp_client
        if running==None:
            running=self.running
        if period==None:
            period = self.period
        if PIDParameters==None:
            PIDParameters=self.PIDParameters
        self.period = period
        self.running=running
        self.PIDParameters=PIDParameters
        parameters = {'running':running,'period':period,'PIDParameters':PIDParameters,'experimentName':self.experimentName}
        pickling_on = open('{}/levelParameters.pickle'.format(self.experimentName),'wb')
        pickle.dump(parameters,pickling_on)
        pickling_on.close()
        ftp_client.put('{}/levelParameters.pickle'.format(self.experimentName),'/home/pi/Documents/levelParameters.pickle')