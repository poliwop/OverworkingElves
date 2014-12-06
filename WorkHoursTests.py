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

def test_timeIntIntersection():
  cases = []

  #Entirely inside bounds
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 1, 11, 2)
  c = dt.datetime(2015, 1, 1, 9, 0)
  d = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b, c, d], 62])

  #Starting too early
  a = dt.datetime(2015, 1, 1, 7, 58)
  b = dt.datetime(2015, 1, 1, 9, 4)
  c = dt.datetime(2015, 1, 1, 8, 0)
  d = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b, c, d], 64])

  #Ending too late
  a = dt.datetime(2015, 1, 1, 15, 4)
  b = dt.datetime(2015, 1, 1, 21, 0)
  c = dt.datetime(2015, 1, 1, 10, 0)
  d = dt.datetime(2015, 1, 1, 20, 5)
  cases.append([[a, b, c, d], 5*60 + 1])

  #Starting too early and ending too late
  a = dt.datetime(2015, 1, 1, 7, 36)
  b = dt.datetime(2015, 1, 1, 21, 1)
  c = dt.datetime(2015, 1, 1, 9, 0)
  d = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b, c, d], 600])

  #Starting too early and ending too early
  a = dt.datetime(2015, 1, 1, 7, 36)
  b = dt.datetime(2015, 1, 1, 8, 1)
  c = dt.datetime(2015, 1, 1, 9, 0)
  d = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b, c, d], 0])

  #Starting too late and ending too late
  a = dt.datetime(2015, 1, 1, 19, 0)
  b = dt.datetime(2015, 1, 1, 20, 1)
  c = dt.datetime(2015, 1, 1, 9, 0)
  d = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b, c, d], 0])

  #Different dates
  a = dt.datetime(2015, 1, 2, 7, 58)
  b = dt.datetime(2015, 1, 1, 9, 4)
  c = dt.datetime(2015, 1, 1, 8, 0)
  d = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b, c, d], -1])

  #Intervals incorrect order
  a = dt.datetime(2015, 1, 1, 15, 4)
  b = dt.datetime(2015, 1, 1, 14, 0)
  c = dt.datetime(2015, 1, 1, 10, 0)
  d = dt.datetime(2015, 1, 1, 20, 5)
  cases.append([[a, b, c, d], -1])

  testFunction(WorkHours.timeIntIntersection, cases)


if __name__ == '__main__':

  test_startOfDay()
  test_endOfDay()
  test_timeIntIntersection()
