import pandas as pd
import matplotlib.pyplot as plt
solnFile = '/home/colin/Desktop/soln/grinch2_015.csv'
toyFile = 'data/toys_rev2.csv'
solnData = pd.read_csv(solnFile)
del solnData['ElfId']
del solnData['StartTime']
solnData.columns = ['ToyId', 'Realtime']
toysData = pd.read_csv(toyFile)
del toysData['Arrival_time']
data = solnData.merge(toysData, on = 'ToyId')
del toysData
sortedData = data.sort(columns='Duration')
del data
#testData = data
subData = sortedData[::500]
del sortedData
subData.plot(kind = 'scatter', x = 'Duration', y = 'Realtime')

plt.show()

#plt.clf()

