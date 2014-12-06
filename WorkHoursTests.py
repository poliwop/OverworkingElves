import datetime as dt
from testCode import *
from WorkHours import *

def test_startOfDay():
  cases = []
  cases.append([[dt.date(2015,1,1)],dt.datetime(2015,1,1,9,0)])
  testFunction(WorkHours.startOfDay, cases)

def test_endOfDay():
  cases = []
  cases.append([[dt.date(2015,1,1)],dt.datetime(2015,1,1,19,0)])
  testFunction(WorkHours.endOfDay, cases)




if __name__ == '__main__':

  test_startOfDay()
  test_endOfDay()
