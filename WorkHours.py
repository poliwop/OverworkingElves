import datetime as dt

class WorkHours:

  dayStart = dt.time(9,0)
  dayEnd = dt.time(19,0)
  workMins = 10*60
  breakMins = 14*60

  @staticmethod
  def startOfDay(day):
    """:param day: date day
       :return: datetime start of work on the day"""
    return dt.datetime.combine(day, WorkHours.dayStart)

  @staticmethod
  def endOfDay(day):
    """:param day: date day
       :return: datetime end of work on the day"""
    return dt.datetime.combine(day, WorkHours.dayEnd)

  @staticmethod
  def timeIntIntersection(a, b, c, d):
    """ Takes two intervals of time, both of which must start and end
    on the same day, and returns intersection in minutes.
    :param a: datetime start of first interval
    :param b: datetime end of first interval
    :param c: datetime start of second interval
    :param d: datetime end of second interval
    :return: int minutes of intersection of intervals, -1 if input 
    does not make sense
    """
    intMins = -1
    if (a.date() == b.date() and a.date() == c.date() and
        a.date() == d.date()) and a < b and c < d:
      if a < d and b > c:
        tdMins = min(b - a, d - a, b - c, d - c)
        intMins = int(tdMins.total_seconds() / 60.0)
      else:
        intMins = 0
    return intMins


  @staticmethod
  def getWorktimes(duration, startTime):
    workEnd = WorkHours.endOfDay(startTime.date())
    jobEnd = startTime + dt.timedelta(minutes = duration)
    if jobEnd <= workEnd:
      return [duration, 0]
    else:
      onMins = int((workEnd - startTime).total_seconds() / 60.0)
      timeLeft = int((jobEnd - workEnd).total_seconds() / 60.0)
      offMins = 0
      while timeLeft >= 1440:		#1440 mins per day
        onMins += Elf.workHours * 60
        offMins += Elf.breakHours * 60
        timeLeft -= 1440
      if timeLeft > Elf.breakHours * 60:
        offMins += Elf.breakHours * 60
        onMins += timeLeft - Elf.breakHours * 60
        timeLeft = 0
      else:
        offMins += timeLeft
        timeLeft = 0
      return [onMins, offMins]




'''
  def getOnMins(startTime, endTime):

    #If both are on same day:
    

    day = startTime.date()
    startToday = max(startTime, WorkHours.startOfDay(day))
    endToday = endTime
    while endToday <= endTime:
      endToday = WorkHours.endOfDay(day)
      onMins = min(endToday - startToday, endTime - startToday)
      day = day + dt.timedelta(days = 1)
      startToday = WorkHours.startOfDay(day)
    

  

  def getOffMins(starTime, endTime):
'''
