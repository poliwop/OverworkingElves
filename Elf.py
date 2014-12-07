import datetime as dt
from WorkHours import *
import math


class Elf:

  minProd = .25
  maxProd = 4.0
  prodIncRate = 1.02
  prodDecRate = .9


  ##### Public Methods #####

  def __init__(self, ID, avail = dt.datetime(2014,1,1,9,0)):
    self.ID = ID
    self.prod = 1.0
    self.available = avail

  def workJob(self, duration, startTime):
    """Work a job of given duration at a given startTime, and update
       internal state accordingly."""
    if startTime < self.available:
      return False
    jobTime = int(math.ceil(duration/self.prod))
    onMins = WorkHours.getApprovedMins(startTime, jobTime)
    offMins = WorkHours.getNonapprovedMins(startTime, jobTime)
    self.adjustAvailability(onMins, offMins, startTime)
    self.adjustProductivity(onMins, offMins)
    return True




  ##### Private Methods #####

  def adjustAvailability(self, onMins, offMins, startTime):
    """Adjust availability based on a number of approved minutes and
    a number of nonapproved minutes."""
    duration = onMins + offMins
    endTime = startTime + dt.timedelta(minutes = duration)
    self.available = WorkHours.addApprovedMins(endTime, offMins)


  def adjustProductivity(self, onMins, offMins):
    """Adjust productivity based on how many minutes elf works during
    sanctioned time, outside sanctioned time."""
    onH = onMins / 60.0
    offH = offMins / 60.0
    newProd = self.prod*(Elf.prodIncRate**onH)*(Elf.prodDecRate**offH)
    newProd = min(newProd, Elf.maxProd)
    self.prod = max(newProd, Elf.minProd)


