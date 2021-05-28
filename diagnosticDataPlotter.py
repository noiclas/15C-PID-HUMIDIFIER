import matplotlib.pyplot as plt
import pickle
import numpy as np

diagnosticInfo = pickle.load(open("diagnosticInfo.pickle", "rb"))
humidities = diagnosticInfo['humidity']
totalErrors = diagnosticInfo['totalError']
pErrors = diagnosticInfo['pError']
iErrors = diagnosticInfo['iError']
times = diagnosticInfo['time']

startTime = times[0]

for i, x in enumerate(times):
    times[i] = x - startTime

plt.subplot(311)
plt.plot(times, humidities)
plt.subplot(312)
plt.plot(times, pErrors, label="pError")
plt.plot(times, iErrors, label="iError")
plt.legend()
plt.subplot(313)
plt.plot(times, totalErrors)
plt.show()