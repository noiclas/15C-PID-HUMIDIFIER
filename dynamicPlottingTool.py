import numpy as np
import matplotlib.pyplot as plt

class dynamicPlotter():
    '''
    Necessary input to initialize dynamicPlotter:
        figure - the matplotlib object where your axes will go (fig - plt.figure())
        (also, have numpy and matplotlib.pyplot imported)
    Optional input to initialize dynamicPlotter:
        'maxMemory, frequency' - the plotter needs an upper bound on how many points it will have to display, so for example if you need it to display up to twelve hours of data at one data point per second you would set maxMemory = 12*60*60 and frequency = 1
    Necessary input to use dynamicPlotter.plot():
        datasets -- in the form datasets = {0:[X0,Y0],1:[X1,Y1],etc}, where each [Xi,Yi] is a full dataset to plot
            -Xi and Yi should have a size of at least two
    Optional input to use dynamicPlotter.plot():
        dataFormat -- in the form dataFormat = {0:{'xlabel':'time'},1:{'memory':600}}.
            This would set the xlabel in the top plot to 'time' and make the second plot display data 600 seconds back
            If you give a custom format, put entries for every graph. For example, if I only want to format the first of two graphs, I could pass dataFormat = {0:{'color':'blue'},1:{}}
        Optional keys to put in each dictionary:
            'memory' - how far back in x you want your data to display, in seconds. Ex: 10 minutes -> 'memory':10
            'xlabel', 'ylabel', 'title', 'color' -- each separate key is a formatting option for each graph
    How to update a parameter:
        self.dataFormat[index]['parameter']=value
    For one set of datasets, initialize one dynamicPlotter. 
    As more data is added to each set, you can call dynamicPlotter.plot() over and over again and it will update the plots.
        
    '''
    def __init__(self,figure,dataFormat=0):
        self.figure=figure
        self.initializePlots = True
        self.dataFormat=dataFormat
        
    def setDefaultParameters(self):
        xlabel = ''
        ylabel = ''
        title = ''
        color = 'blue'
        maxMemory = 1*60*60
        memory=50
        frequency = 50
        defaultFormat = {i:{'memory':memory,'xlabel':xlabel,'ylabel':ylabel,'color':color,'title':title,'maxMemory':maxMemory,'frequency':frequency} for i in range(0,self.numberOfAxes)}
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
        for index in range(0,self.numberOfAxes):
            self.dataFormat[index]['frequency'] = 4 * self.dataFormat[index]['frequency']
        
        
    def createAxes(self):
        self.axes = {i:0 for i in range(0,self.numberOfAxes)}
        self.plotters = {i:0 for i in range(0,self.numberOfAxes)}
        for index in range(0,self.numberOfAxes):
            self.axes[index] = self.figure.add_subplot(self.numberOfAxes,1,index+1)
        for index in range(0,self.numberOfAxes):
            self.plotters[index] = dynamicSinglePlot(self.figure,self.axes[index],color=self.dataFormat[index]['color'])
            self.plotters[index].setFormatting(xlabel = self.dataFormat[index]['xlabel'],ylabel = self.dataFormat[index]['ylabel'],maxMemory = self.dataFormat[index]['maxMemory'],frequency = self.dataFormat[index]['frequency'],title=self.dataFormat[index]['title'],memory=self.dataFormat[index]['memory'])
        self.figure.tight_layout(h_pad=2)
        plt.subplots_adjust(top=0.9)
        
    def plot(self,datasets):
        if self.initializePlots == False:
            for index in range(0,self.numberOfAxes):
                self.plotters[index].setFormatting(xlabel = self.dataFormat[index]['xlabel'],ylabel = self.dataFormat[index]['ylabel'],maxMemory = self.dataFormat[index]['maxMemory'],frequency = self.dataFormat[index]['frequency'],title=self.dataFormat[index]['title'],memory=self.dataFormat[index]['memory'])
                self.plotters[index].updatePlot(datasets[index][0],datasets[index][1])
        else:
            self.numberOfAxes = len(datasets)
            self.setDefaultParameters()
            self.initializePlots = False
            self.createAxes()
            for index in range(0,self.numberOfAxes):
                self.plotters[index].initializePlot(datasets[index][0],datasets[index][1])
    
    
        
        
        


class dynamicSinglePlot():
    '''
    This class deals with one set of variables x=[x1,x2,...] and y=[y1,y2,...] 
    and plots them on a given axis with some user-inputted parameters like labels 
    and the range of data to 
    display at a given time (for example, data over the last 10 minutes). As more (x,y)
    are collected, it can update the plot, creating a real-time graph of the
    data.
    '''
    
    def __init__(self,figure,axis,color='blue'):
        self.figure = figure
        self.axis = axis
        self.color = color
    
    def setFormatting(self,xlabel,ylabel,title,maxMemory,memory,frequency = 5):
        self.axis.set_xlabel(xlabel)
        self.axis.set_ylabel(ylabel)
        self.axis.set_title(title)
        self.maxMemory = maxMemory
        self.frequency = frequency
        self.memory = memory
    
    def setFormat(self,x,y):
        y = np.array(y)
        x=np.array(x)
        #setting limits of graph
        rightmostXLim = x[-1]
        leftmostDataPoint = x[0]
        if rightmostXLim - leftmostDataPoint <= self.memory:
            leftmostXLim = leftmostDataPoint
        else:
            leftmostXLim = rightmostXLim - self.memory
        xInRange = x[x>=(leftmostXLim*0.9)]
        yInRange = y[x>=(leftmostXLim*0.9)]
        xLim = [leftmostXLim,rightmostXLim+0.2*(rightmostXLim-leftmostXLim)]
        yMin = np.min(yInRange)
        yMax = np.max(yInRange)
        yRange = yMax-yMin
        yLim = [yMin - yRange*0.2,yMax + yRange*0.2]
        if np.size(x)==1:
            xLim = [x[0]-1,x[0]+1]
            yLim = [y[0]-1,y[0]+1]
        self.axis.set_xlim(xLim)
        self.axis.set_ylim(yLim)
        
        #finding x and y to plot; it needs to artificially have a constant length even when we change the data so we have to
        #cut it do what's in our plotting window then put a pad on the end that won't be displayed
        numberOfPoints = self.maxMemory * self.frequency
        pad = np.ones(numberOfPoints-len(xInRange))
        xToPlot = np.concatenate((pad*0.9*leftmostXLim,xInRange))
        yToPlot = np.concatenate((pad,yInRange))
        return xToPlot, yToPlot
        
    def initializePlot(self,x,y):
        xToPlot, yToPlot = self.setFormat(x,y)
        self.lines = self.axis.plot(xToPlot,yToPlot, color = self.color)
        #self.axis.legend()
    
    def updatePlot(self,x,y):
        xToPlot, yToPlot = self.setFormat(x,y)
        self.lines[0].set_xdata(xToPlot)
        self.lines[0].set_ydata(yToPlot)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        
    
 

