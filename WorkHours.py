import datetime as dt

class WorkHours:

  dayStart = dt.time(9,0)
  dayEnd = dt.time(19,0)
  workMins = 10*60
  breakMins = 14*60

  @staticmethod
  def startOfDay(day):
    return dt.datetime.combine(day, WorkHours.dayStart)

  @staticmethod
  def endOfDay(day):
    return dt.datetime.combine(day, WorkHours.dayEnd)
