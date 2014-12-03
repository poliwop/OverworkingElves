from santaUtil import *


class Elf:

  dayStart = dt.time(9,0)
  dayEnd = dt.time(19,0)
  workHours = 10
  breakHours = 14
  minProd = .25
  maxProd = 4.0

  def __init__(self, ID):
    self.ID = ID
    self.prod = 1.0
    self.available = dt.datetime(2014,1,1,9,0)

  def workJob(self, duration, startTime):
    if startTime < self.available or startTime > self.endOfDay(startTime.date()):
      return False
    jobTime = actualDuration(duration, self.prod)
    [onMins, offMins] = self.calcWorktimes(jobTime, startTime)
    self.adjustAvailability(onMins, offMins, startTime)
    self.adjustProductivity(onMins, offMins)
    return True

  def adjustAvailability(self, onMins, offMins, startTime):
    duration = onMins + offMins
    endTime = addTime(duration, startTime)
    nextAvailable = endTime
    if endTime >= self.endOfDay(startTime.date()):
      daysToAdd = 1 + offMins // 600
      minsToAdd = offMins % 600
      nextAvailable += dt.timedelta(days = daysToAdd)
      nextAvailable = self.startOfDay(nextAvailable.date())
      nextAvailable += dt.timedelta(minutes = minsToAdd)
    self.available = nextAvailable

  def adjustProductivity(self, onMins, offMins):
    onHours = onMins / 60.0
    offHours = offMins / 60.0
    newProd = self.prod * (1.02**onHours) * (.9**offHours)
    newProd = min(newProd, Elf.maxProd)
    self.prod = max(newProd, Elf.minProd)

  def calcWorktimes(self, duration, startTime):
    workEnd = self.endOfDay(startTime.date())
    jobEnd = addTime(duration, startTime)
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

  def startOfDay(self, day):
    return self.timeOnDay(day, Elf.dayStart)

  def endOfDay(self, day):
    return self.timeOnDay(day, Elf.dayEnd)

  def timeOnDay(self, day, time):
    return dt.datetime.combine(day, time)
