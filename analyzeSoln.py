import pandas as pd
import matplotlib.pyplot as plt
solnFile = 'soln/grinch008.csv'
toyFile = 'data/toys_rev2.csv'
solnData = pd.read_csv(solnFile)
del solnData['ElfId']
del solnData['StartTime']
solnData.columns = ['ToyId', 'Realtime']
toysData = pd.read_csv(toyFile)
del toysData['Arrival_time']
data = solnData.merge(toysData, on = 'ToyId')
sortedData = data.sort(columns='Duration')
#testData = data
subData = sortedData[::500]
subData.plot(kind = 'scatter', x = 'Duration', y = 'Realtime')


secondData = sortedData[1000000:1100000]

thirdData = sortedData[1100000:1200000]

data.plot(kind='scatter', x = 'Duration', y = 'Realtime')

firstData.plot(kind='scatter', x = 'Duration', y = 'Realtime')

secondData.plot('Duration', 'Realtime', '.')

thirdData.plot('Duration', 'Realtime', '.')

plt.show()

plt.clf()

