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

def test_isApproved():
  cases = []
  cases.append([[dt.datetime(2015,1,1,1,0)],False])
  cases.append([[dt.datetime(2015,1,1,9,0)],True])
  cases.append([[dt.datetime(2015,1,1,11,27)],True])
  cases.append([[dt.datetime(2015,1,1,19,0)],False])
  cases.append([[dt.datetime(2015,1,1,21,2)],False])
  cases.append([[dt.datetime(2015,1,1,0,0)],False])
  testFunction(WorkHours.isApproved, cases)


def test_nextApproved():
  cases = []
  cases.append([[dt.datetime(2015,1,1,1,0)],dt.datetime(2015,1,1,9,0)])
  cases.append([[dt.datetime(2015,1,1,9,0)],dt.datetime(2015,1,1,9,0)])
  cases.append([[dt.datetime(2015,1,1,11,27)],dt.datetime(2015,1,1,11,27)])
  cases.append([[dt.datetime(2015,1,1,19,0)],dt.datetime(2015,1,2,9,0)])
  cases.append([[dt.datetime(2015,1,1,21,2)],dt.datetime(2015,1,2,9,0)])
  cases.append([[dt.datetime(2015,1,1,0,0)],dt.datetime(2015,1,1,9,0)])
  testFunction(WorkHours.nextApproved, cases)


def test_onSameDay():
  cases = []
  #same date
  cases.append([[dt.datetime(2014,1,1,9,0),
                 dt.datetime(2014,1,1,9,5)],True])
  #different date
  cases.append([[dt.datetime(2014,1,2,9,0),
                 dt.datetime(2014,1,1,9,5)],False])
  #one midnight
  cases.append([[dt.datetime(2014,1,1,9,0),
                 dt.datetime(2014,1,2,0,0)],True])
  #two midnights, same date
  cases.append([[dt.datetime(2014,1,1,0,0),
                 dt.datetime(2014,1,2,0,0)],True])
  #two midnights, different date
  cases.append([[dt.datetime(2014,1,1,0,0),
                 dt.datetime(2014,1,3,0,0)],False])
  testFunction(WorkHours.onSameDay, cases)

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

  #Ending at midnight
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 2, 0, 0)
  c = dt.datetime(2015, 1, 1, 9, 0)
  d = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b, c, d], 9*60])

  #All day
  a = dt.datetime(2015, 1, 1, 0, 0)
  b = dt.datetime(2015, 1, 2, 0, 0)
  c = dt.datetime(2015, 1, 1, 9, 0)
  d = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b, c, d], 600])

  testFunction(WorkHours.timeIntIntersection, cases)


def test_getDayOnMinutes():
  cases = []

  #All day
  a = dt.datetime(2015, 1, 1, 0, 0)
  b = dt.datetime(2015, 1, 2, 0, 0)
  cases.append([[a, b], 600])

  #start during day
  a = dt.datetime(2015, 1, 1, 11, 23)
  b = dt.datetime(2015, 1, 1, 20, 0)
  cases.append([[a, b], 7*60 + 37])

  #end during day
  a = dt.datetime(2015, 1, 1, 1, 0)
  b = dt.datetime(2015, 1, 1, 17, 0)
  cases.append([[a, b], 8*60])

  #all onHours
  a = dt.datetime(2015, 1, 1, 2, 0)
  b = dt.datetime(2015, 1, 1, 21, 0)
  cases.append([[a, b], 600])

  #go to midnight
  a = dt.datetime(2015, 1, 1, 17, 1)
  b = dt.datetime(2015, 1, 2, 0, 0)
  cases.append([[a, b], 119])

  testFunction(WorkHours.getDayOnMinutes, cases)

def test_getDayOffMinutes():
  cases = []

  #All day
  a = dt.datetime(2015, 1, 1, 0, 0)
  b = dt.datetime(2015, 1, 2, 0, 0)
  cases.append([[a, b], 14*60])

  #start during day
  a = dt.datetime(2015, 1, 1, 11, 23)
  b = dt.datetime(2015, 1, 1, 20, 0)
  cases.append([[a, b], 60])

  #end during day
  a = dt.datetime(2015, 1, 1, 1, 0)
  b = dt.datetime(2015, 1, 1, 17, 0)
  cases.append([[a, b], 8*60])

  #start early, end late
  a = dt.datetime(2015, 1, 1, 2, 0)
  b = dt.datetime(2015, 1, 1, 21, 0)
  cases.append([[a, b], 7*60 + 2*60])

  #start late, end early
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 1, 18, 0)
  cases.append([[a, b], 0])

  testFunction(WorkHours.getDayOffMinutes, cases)


def test_getOnMinutes():
  cases = []

  #Short job
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 1, 18, 0)
  cases.append([[a, b], 8*60])

  #Full day job
  a = dt.datetime(2015, 1, 1, 9, 0)
  b = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b], 600])

  #start early
  a = dt.datetime(2015, 1, 1, 8, 0)
  b = dt.datetime(2015, 1, 1, 18, 0)
  cases.append([[a, b], 540])

  #end late
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 1, 20, 0)
  cases.append([[a, b], 540])

  #Multiple days:
  #start and end during day hours
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 3, 18, 30)
  cases.append([[a, b], 540 + 600 + 570])

  #start during day, end at night
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 4, 21, 30)
  cases.append([[a, b], 540 + 600*3])

  #start during night, end at day
  a = dt.datetime(2015, 1, 1, 21, 0)
  b = dt.datetime(2015, 1, 4, 17, 30)
  cases.append([[a, b], 600*2 + 8*60 + 30])

  #start during night, end at night
  a = dt.datetime(2015, 1, 1, 21, 0)
  b = dt.datetime(2015, 1, 7, 23, 30)
  cases.append([[a, b], 600*6])

  #end next day
  a = dt.datetime(2015, 1, 1, 17, 1)
  b = dt.datetime(2015, 1, 2, 13, 2)
  cases.append([[a, b], 119 + 4*60 + 2])

  #all off hours
  a = dt.datetime(2015, 1, 1, 21, 1)
  b = dt.datetime(2015, 1, 2, 5, 2)
  cases.append([[a, b], 0])

  #go to midnight
  a = dt.datetime(2015, 1, 1, 17, 1)
  b = dt.datetime(2015, 1, 2, 0, 0)
  cases.append([[a, b], 119])

  testFunction(WorkHours.getOnMinutes, cases)


def test_getOffMinutes():
  cases = []

  #Short job
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 1, 18, 0)
  cases.append([[a, b], 0])

  #Full day job
  a = dt.datetime(2015, 1, 1, 9, 0)
  b = dt.datetime(2015, 1, 1, 19, 0)
  cases.append([[a, b], 0])

  #start early
  a = dt.datetime(2015, 1, 1, 8, 0)
  b = dt.datetime(2015, 1, 1, 18, 0)
  cases.append([[a, b], 60])

  #end late
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 1, 20, 0)
  cases.append([[a, b], 60])

  #Multiple days:
  #start and end during day hours
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 3, 18, 30)
  cases.append([[a, b], (5 + 9 + 5 + 9)*60])

  #start during day, end at night
  a = dt.datetime(2015, 1, 1, 10, 0)
  b = dt.datetime(2015, 1, 4, 21, 30)
  cases.append([[a, b], (5*3 + 9*3)*60 + 150])

  #start during night, end at day
  a = dt.datetime(2015, 1, 1, 21, 0)
  b = dt.datetime(2015, 1, 4, 17, 30)
  cases.append([[a, b], (3 + 3*9 + 2*5)*60])

  #start during night, end at night
  a = dt.datetime(2015, 1, 1, 21, 0)
  b = dt.datetime(2015, 1, 7, 23, 30)
  cases.append([[a, b], (3 + 6*9 + 5*5)*60 + 4*60 + 30])

  #end next day
  a = dt.datetime(2015, 1, 1, 17, 1)
  b = dt.datetime(2015, 1, 2, 13, 2)
  cases.append([[a, b], 14*60])

  #all off hours
  a = dt.datetime(2015, 1, 1, 21, 1)
  b = dt.datetime(2015, 1, 2, 5, 2)
  cases.append([[a, b], 179 + 302])

  #go to midnight
  a = dt.datetime(2015, 1, 1, 17, 1)
  b = dt.datetime(2015, 1, 2, 0, 0)
  cases.append([[a, b], 5*60])

  testFunction(WorkHours.getOffMinutes, cases)


def test_getApprovedMins():
  cases = []

  #All approved
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 150], 150])

  #Full day job
  a = dt.datetime(2015, 1, 1, 9, 0)
  cases.append([[a, 600], 600])

  #start early
  a = dt.datetime(2015, 1, 1, 8, 0)
  cases.append([[a, 600], 540])

  #end late
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 780], 540])

  #Long jobs:
  #start and end during day hours
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 1440*3 + 3], 600*3 + 3])

  #start during day, end at night
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 1440*4 + 700], 600*4 + 540])

  #go to midnight
  a = dt.datetime(2015, 1, 1, 17, 1)
  cases.append([[a, 7*60 - 1], 119])

  testFunction(WorkHours.getApprovedMins, cases)


def test_getNonapprovedMins():
  cases = []

  #All approved
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 150], 0])

  #Full day job
  a = dt.datetime(2015, 1, 1, 9, 0)
  cases.append([[a, 600], 0])

  #start early
  a = dt.datetime(2015, 1, 1, 8, 0)
  cases.append([[a, 600], 60])

  #end late
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 780], 240])

  #Long jobs:
  #start and end during day hours
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 1440*3 + 3], 840*3])

  #start during day, end at night
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 1440*4 + 700], 840*4 + 160])

  #go to midnight
  a = dt.datetime(2015, 1, 1, 17, 1)
  cases.append([[a, 7*60 - 1], 300])

  testFunction(WorkHours.getNonapprovedMins, cases)


def test_addApprovedMins():
  cases = []

  #All approved
  a = dt.datetime(2015, 1, 1, 10, 0)
  cases.append([[a, 100], dt.datetime(2015, 1, 1, 11, 40)])

  #Next day
  a = dt.datetime(2015, 1, 1, 18, 0)
  cases.append([[a, 120], dt.datetime(2015, 1, 2, 10, 0)])

  #Ends at endOfDay
  a = dt.datetime(2015, 1, 1, 18, 0)
  cases.append([[a, 60], dt.datetime(2015, 1, 2, 9, 0)])

  testFunction(WorkHours.addApprovedMins, cases)


if __name__ == '__main__':

  test_startOfDay()
  test_endOfDay()
  test_isApproved()
  test_nextApproved()
  test_onSameDay()
  test_timeIntIntersection()
  test_getDayOnMinutes()
  test_getDayOffMinutes()
  test_getOnMinutes()
  test_getOffMinutes()
  test_getApprovedMins()
  test_getNonapprovedMins()
  test_addApprovedMins()
