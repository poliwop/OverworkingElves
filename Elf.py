from santaUtil import *
from WorkHours import *


class Elf:

  minProd = .25
  maxProd = 4.0
  prodIncRate = 1.02
  prodDecRate = .9

  def __init__(self, ID, avail = dt.datetime(2014,1,1,9,0)):
    self.ID = ID
    self.prod = 1.0
    self.available = avail

  def workJob(self, duration, startTime):
    if startTime < self.available or startTime > WorkHours.endOfDay(startTime.date()):
      return False
    jobTime = actualDuration(duration, self.prod)
    [onMins, offMins] = self.getWorktimes(jobTime, startTime)
    self.adjustAvailability(onMins, offMins, startTime)
    self.adjustProductivity(onMins, offMins)
    return True

  def adjustAvailability(self, onMins, offMins, startTime):
    duration = onMins + offMins
    endTime = addTime(duration, startTime)
    nextAvailable = endTime
    if endTime >= self.endOfDay(startTime.date()):
      nextAvailable = self.nextMorning(endTime)
      daysToAdd = offMins // 600
      minsToAdd = offMins % 600
      nextAvailable += dt.timedelta(days = daysToAdd)
      nextAvailable = self.startOfDay(nextAvailable.date())
      nextAvailable += dt.timedelta(minutes = minsToAdd)
    self.available = nextAvailable

  def nextMorning(self, fromTime):
    morning = dt.datetime.combine(fromTime.date(), Elf.dayStart)
    if fromTime > morning:
      morning = morning + dt.timedelta(days = 1)
    return morning





  #Utilities

  def adjustProductivity(self, onMins, offMins):
    """Adjust productivity based on how many minutes elf works during
    sanctioned time, outside sanctioned time.
    :param onMins: int minutes worked during sanctioned time
    :param offMins: int minutes worked outside sanctioned time
    """
    onH = onMins / 60.0
    offH = offMins / 60.0
    newProd = self.prod*(Elf.prodIncRate**onH)*(Elf.prodDecRate**offH)
    newProd = min(newProd, Elf.maxProd)
    self.prod = max(newProd, Elf.minProd)


