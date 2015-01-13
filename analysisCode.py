'''
OverworkingElves: a solution to the Kaggle 2014 Christmas optimization competition.
Copyright 2014 Colin Grove. See README for more info.
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
toyFile = 'data/toys_rev2.csv'
toysData = pd.read_csv(toyFile)
del toysData['Arrival_time']
binwidth = 1000

ax1 = toysData.hist(column = 'Duration', bins=range(0, 25000, binwidth), xlab = "Job Duration")

toysData['bin'] = map(getGroupingFunction(binwidth), toysData['Duration'])*binwidth
#toysData['bin'] = toysData['bin']*binwidth
grouped = toysData.groupby('bin')
minsInBins = grouped['Duration'].aggregate(np.sum)
ax2 = minsInBins.plot(kind = 'bar')
ax2.set_xlabel("Job Duration (in minutes)")
ax2.set_ylabel("Job-minutes (in billions)")
ax2.set_title("Job-minutes by Durations of Jobs")

plt.show()

def getGroupingFunction(n):
  return lambda x: x / n
