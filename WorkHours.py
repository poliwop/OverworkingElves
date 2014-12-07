import datetime as dt

class WorkHours:

  dayStart = dt.time(9,0)
  dayEnd = dt.time(19,0)
  workMins = 10*60
  breakMins = 14*60


  ##### Public Methods #####

  @staticmethod
  def getApprovedMins(startTime, duration):
    """Returns approved minutes in duration after startTime."""
    endTime = startTime + dt.timedelta(minutes = duration)
    return WorkHours.getOnMinutes(startTime, endTime)

  @staticmethod
  def getNonapprovedMins(startTime, duration):
    """Returns nonapproved minutes in duration after startTime."""
    return duration - WorkHours.getApprovedMins(startTime, duration)

  @staticmethod
  def addApprovedMins(startTime, duration):
    """Adds approved minutes of length duration to startTime, returns
       next approved minute."""
    timeLeft = duration
    currentTime = WorkHours.nextApproved(startTime)
    while timeLeft > 0:
      minsLeftToday = WorkHours.endOfDay(currentTime) - currentTime
      minsAddToday = min(minsLeftToday, dt.timedelta(minutes = timeLeft))
      currentTime = WorkHours.nextApproved(currentTime + minsAddToday)
      timeLeft -= int(minsAddToday.total_seconds()/60.0)
    return currentTime

  @staticmethod
  def nextApproved(startTime):
    """Returns next approved time."""
    next = startTime
    if next < WorkHours.startOfDay(next):
      next = WorkHours.startOfDay(next)
    elif next >= WorkHours.endOfDay(next):
      next = WorkHours.startOfDay(next + dt.timedelta(days = 1))
    return next

  @staticmethod
  def isApproved(startTime):
    """Indicates whether startTime is approved."""
    lateEnough = (startTime >= WorkHours.startOfDay(startTime))
    earlyEnough = (startTime < WorkHours.endOfDay(startTime))
    return lateEnough and earlyEnough

  @staticmethod
  def startOfDay(day):
    """Returns start of workday on day as datetime."""
    return dt.datetime.combine(day, WorkHours.dayStart)

  @staticmethod
  def endOfDay(day):
    """Returns end of workday on day as datetime."""
    return dt.datetime.combine(day, WorkHours.dayEnd)




  ##### Private Methods #####

  @staticmethod
  def getOnMinutes(startTime, endTime):
    """Returns number of approved minutes in time interval."""
    totalMins = 0
    if startTime <= endTime:
      currentDay = startTime.date()
      while currentDay <= endTime.date():
        #calc start time
        thisMorning = dt.datetime.combine(currentDay, dt.time(0,0))
        startHour = max(startTime, thisMorning)
        #calc end time
        thisNight = dt.datetime.combine(currentDay + dt.timedelta(days = 1),
                                        dt.time(0,0))
        endHour = min(endTime, thisNight)
        #add on minutes for day
        totalMins += WorkHours.getDayOnMinutes(startHour, endHour)
        #update currentDay
        currentDay = currentDay + dt.timedelta(days = 1)
    return totalMins

  @staticmethod
  def getOffMinutes(startTime, endTime):
    """Returns number of nonapproved minutes in time interval."""
    offMins = 0
    if startTime <= endTime:
      totalMins = int((endTime - startTime).total_seconds()/60.0)
      offMins = totalMins - WorkHours.getOnMinutes(startTime, endTime)
    return offMins


  @staticmethod
  def getDayOnMinutes(startTime, endTime):
    """Returns number of approved minutes in time interval, which must
       be an interval on a single day."""
    startToday = WorkHours.startOfDay(startTime.date())
    endToday = WorkHours.endOfDay(startTime.date())
    return WorkHours.timeIntIntersection(startTime, endTime,
                                         startToday, endToday)

  @staticmethod
  def getDayOffMinutes(startTime, endTime):
    """Returns number of nonapproved minutes in time interval, which must
       be an interval on a single day."""
    totalMins = int((endTime - startTime).total_seconds()/60.0)
    onMins = WorkHours.getDayOnMinutes(startTime, endTime)
    offMins = totalMins - onMins
    if onMins == -1:
      offMins = -1
    return offMins


  @staticmethod
  def timeIntIntersection(a, b, c, d):
    """Takes two time intervals and returns the length of the intersection,
       in minutes, or -1 if the input does not make sense."""
    intMins = -1
    #check if intervals start on same day, make sense
    if (a.date() == c.date()) and a <= b and c <= d:
      #check if intervals end on same day they start, or at midnight
      if WorkHours.onSameDay(a,b) and WorkHours.onSameDay(c,d):
        #check if intervals overlap at all
        if a <= d and b >= c:
          tdMins = min(b - a, d - a, b - c, d - c)
          intMins = int(tdMins.total_seconds() / 60.0)
        else:
          intMins = 0
    return intMins


  @staticmethod
  def onSameDay(a, b):
    """Checks if two datetimes are on the same day, where midnight can
       be considered in either day."""
    c = min(a, b)
    d = max(a, b)
    cMidnight = dt.datetime.combine(c.date()+dt.timedelta(days=1),dt.time(0,0))
    return c.date() == d.date() or (d - c == cMidnight - c)



