import numpy as np
import matplotlib.pyplot as plt

class dynamicPlotter():
    '''
    Give datasets = {0:[X,Y0,Y1,Y2,...],1:[X,Y0,Y1,...],...} to call dynamicPlotter.plot(datasets)
    Give dataFormat = {0:{'memory':memory},1:{}} to initialize dynamicPlotter
    '''
    def __init__(self,figure,dataFormat=0):
        self.figure=figure
        self.initializePlots = True
        self.dataFormat=dataFormat
        
    def setDefaultParameters(self):
        xlabel = ''
        ylabel = ''
        title = ''
        colors = 0
        labels = 0
        maxMemory = 1*60*60
        memory=1000
        frequency = 50
        defaultFormat = {i:{'memory':memory,'xlabel':xlabel,'ylabel':ylabel,'colors':colors,'title':title,'maxMemory':maxMemory,'frequency':frequency,'labels':labels} for i in range(0,self.numberOfAxes)}
        if self.dataFormat == 0 :
            self.dataFormat = defaultFormat
        else:
            for index in range(0,self.numberOfAxes):
                keys = list(defaultFormat[index].keys())
                for key in keys:
                    try:
                        self.dataFormat[index][key]
                    except:
                        self.dataFormat[index][key]=defaultFormat[index][key]
        if self.initializePlots == True:
            for index in range(0,self.numberOfAxes):
                self.dataFormat[index]['frequency'] = 4 * self.dataFormat[index]['frequency']
        
        
    def createAxes(self):
        self.axes = {i:0 for i in range(0,self.numberOfAxes)}
        self.plotters = {i:0 for i in range(0,self.numberOfAxes)}
        for index in range(0,self.numberOfAxes):
            self.axes[index] = self.figure.add_subplot(self.numberOfAxes,1,index+1)
        for index in range(0,self.numberOfAxes):
            self.plotters[index] = dynamicSinglePlot(self.figure,self.axes[index],colors=self.dataFormat[index]['colors'],maxMemory = self.dataFormat[index]['maxMemory'],frequency = self.dataFormat[index]['frequency'],labels=self.dataFormat[index]['labels'])
            self.plotters[index].setFormatting(xlabel = self.dataFormat[index]['xlabel'],ylabel = self.dataFormat[index]['ylabel'],title=self.dataFormat[index]['title'],memory=self.dataFormat[index]['memory'])
        self.figure.tight_layout(h_pad=1)
        plt.subplots_adjust(top=0.9)
        
    def plot(self,datasets):
        if self.initializePlots == False:
            for index in range(0,self.numberOfAxes):
                x = datasets[index][0]
                y = [datasets[index][i] for i in range(1,len(datasets[index]))]
                self.plotters[index].setFormatting(xlabel = self.dataFormat[index]['xlabel'],ylabel = self.dataFormat[index]['ylabel'],title=self.dataFormat[index]['title'],memory=self.dataFormat[index]['memory'])
                self.plotters[index].updatePlot(x,y)
        else:
            self.numberOfAxes = len(datasets)
            self.setDefaultParameters()
            self.initializePlots = False
            self.createAxes()
            for index in range(0,self.numberOfAxes):
                x = datasets[index][0]
                y = [datasets[index][i] for i in range(1,len(datasets[index]))]
                self.plotters[index].initializePlot(x,y)
    
    
        
        
        


class dynamicSinglePlot():
    '''
    This class deals with one set of variables x=[x1,x2,...] and y=[y1,y2,...] 
    and plots them on a given axis with some user-inputted parameters like labels 
    and the range of data to 
    display at a given time (for example, data over the last 10 minutes). As more (x,y)
    are collected, it can update the plot, creating a real-time graph of the
    data.
    '''
    
    def __init__(self,figure,axis,colors=0,labels=0,maxMemory=3600,frequency=50):
        self.figure = figure
        self.axis = axis
        self.colors = colors
        self.maxMemory = maxMemory
        self.frequency = frequency
        self.labels = labels

    def setFormatting(self,xlabel,ylabel,title,memory):
        self.axis.set_xlabel(xlabel)
        self.axis.set_ylabel(ylabel)
        self.axis.set_title(title)
        self.memory = memory
    
    def setFormat(self,x,Y):
        Y = [np.array(y) for y in Y]
        x=np.array(x)
        #setting limits of graph
        rightmostXLim = x[-1]
        leftmostDataPoint = x[0]
        if rightmostXLim - leftmostDataPoint <= self.memory:
            leftmostXLim = leftmostDataPoint
        else:
            leftmostXLim = rightmostXLim - self.memory
        xInRange = x[x>=(leftmostXLim*0.9)]
        xLim = [leftmostXLim,rightmostXLim+0.2*(rightmostXLim-leftmostXLim)]
        yInRange = [y[x>=(leftmostXLim*0.9)] for y in Y]
        yMin = np.min([np.min(y) for y in yInRange])
        yMax = np.max([np.max(y) for y in yInRange])
        yRange = yMax-yMin
        yLim = [yMin - yRange*0.2,yMax + yRange*0.2]
        if np.size(x)==1:
            xLim = [x[0]-1,x[0]+1]
            yLim = [Y[0][0]-1,Y[0][0]+1]
        if yMin == yMax:
            yLim = [yMin*0.9,yMin*1.1]
        self.axis.set_xlim(xLim)
        self.axis.set_ylim(yLim)
        
        #finding x and y to plot; it needs to artificially have a constant length even when we change the data so we have to
        #cut it do what's in our plotting window then put a pad on the end that won't be displayed
        numberOfPoints = self.maxMemory * self.frequency
        pad = np.ones(numberOfPoints-len(xInRange))
        xToPlot = np.concatenate((pad*0.9*leftmostXLim,xInRange))
        yToPlot = [np.concatenate((pad,y)) for y in yInRange]
        return xToPlot, yToPlot
        
    def initializePlot(self,x,y):
        xToPlot, yToPlot = self.setFormat(x,y)
        self.lines = [self.axis.plot(xToPlot,y) for y in yToPlot]
        if self.colors != 0:
            for index in range(0,len(self.lines)):
                self.lines[index][0].set_color(self.colors[index])
        if self.labels != 0:
            for index in range(0,len(self.lines)):
                self.lines[index][0].set_label(self.labels[index])
            self.axis.legend()
        
    
    def updatePlot(self,x,y):
        xToPlot, yToPlot = self.setFormat(x,y)
        for i in range(0,len(yToPlot)):
            self.lines[i][0].set_xdata(xToPlot)
            self.lines[i][0].set_ydata(yToPlot[i])
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        
'''
import time
fig = plt.figure()
dataFormat = {0:{'colors':['red','yellow','green'],'labels':['redline','yellowline','greenline']}}
plotter=dynamicPlotter(figure=fig,dataFormat=dataFormat)
datasets = {0:[[0,1,2],[-1,0,1],[1,2,3],[2,3,4]]}
plotter.plot(datasets)
time.sleep(0.2)
datasets = {0:[[0,1,2,3],[-1,0,1,3],[1,2,3,3],[2,3,4,3]]}
plotter.plot(datasets)
'''

