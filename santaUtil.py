import datetime as dt
import math


def addTime(duration, time):
  return time + dt.timedelta(minutes = duration)

def actualDuration(duration, prod):
  return int(math.ceil(duration/prod))


