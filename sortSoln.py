import pandas as pd
import datetime as dt
solnPath = '/home/colin/Desktop/soln/'
solnFile = 'grinch2_018'
outFile = solnFile + '_sorted'

def toDateString(daytime):
  """Reformats datetime into approriate datestring format for sumbssion."""
  daytime = dt.datetime.strptime(daytime, "%Y-%m-%d %H:%M:%S")
  dayStr = " ".join([str(daytime.year), str(daytime.month), str(daytime.day)])
  timeStr = " ".join([str(daytime.hour), str(daytime.minute)])
  return dayStr + " " + timeStr

if __name__ == '__main__':

  solnData = pd.read_csv(solnPath + solnFile + '.csv')
  solnData.columns = ['ToyId', 'ElfId', 'StartTime', 'Duration']
  sortedData = solnData.sort(columns='StartTime')
  sortedData['StartTime'] = sortedData.StartTime.apply(toDateString)
  sortedData.to_csv(solnPath + outFile + '.csv', index = False)


#  with open(solnFile, 'wb') as w:
#    solnWriter = csv.writer(w)
#    solnWriter.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])
#    w.writerow(jobOut)
