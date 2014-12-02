
from santaUtil import *
from Elf import *
#import pandas as pd
import numpy as np
import csv as csv
from operator import itemgetter

toyFile = 'data/toys_rev2.csv'
solnFile = 'soln/submission.csv'
WORKFORCE = 900
BIG_PROD = 2.0
REF_DT = dt.datetime(2014,1,1,0,0)
START_DATE = dt.date(2014,12,11)

# Methods for setup

def toDatetime(data, col):
  orderTime = []
  for timestamp in data[col]:
    splitStamp = map(int, timestamp.split(' '))
    date = dt.datetime(*splitStamp)
    orderTime.append( date )
  data[col] = orderTime

def toDateString(daytime):
  dayStr = " ".join([str(daytime.year), str(daytime.month), str(daytime.day)])
  timeStr = " ".join([str(daytime.hour), str(daytime.minute)])
  return dayStr + " " + timeStr

def addJobToList(jobslist, jobID, duration):
  while len(jobslist) <= duration:
    jobslist.append([])
  jobslist[duration].append(jobID)

def getJobFromList(jobslist, duration):
  if len(jobslist) > duration and len(jobslist[duration]) > 0:
    jobID = jobslist[duration].pop(0)
    while len(jobslist) > 0 and len(jobslist[-1]) == 0:
      jobslist.pop()
    return jobID
  else:
    return False

def assignJobToElf(elf, duration, startTime, jobslist):
  jobID = getJobFromList(jobslist, duration)
  elf.workJob(duration, startTime)
  return [jobID, elf.ID, startTime, duration]

def scheduleElfDay(elf, jobs, date):
  elfJobs = []
  bigJob = len(jobs) - 1
  if elf.available.date() < date:
    elf.available = elf.startOfDay(date)
  if elf.available < elf.endOfDay(date):
    '''
    if bigJob > 150 and timeFromMin(elf.prod)*10 >= bigJob:
      job = assignJobToElf(elf, bigJob, elf.available, jobs)
      elfJobs.append(job)

    else:
    '''
    bestDuration = min(getBestDuration(elf, date, bigJob), len(jobs) - 1)
#    print(bestDuration)
    while bestDuration > 0:
      bigJob = len(jobs) - 1
      desProd = desiredProd(bigJob)
#      print([elf.prod, desProd])
      if elf.prod >= desProd:
        bestDuration = bigJob
      if len(jobs[bestDuration]) > 0:
        job = assignJobToElf(elf, bestDuration, elf.available, jobs)
        elfJobs.append(job)
        bestDuration = min(getBestDuration(elf, date, bigJob), len(jobs) - 1)
      else:
        bestDuration -= 1
  return elfJobs

#def getBestDuration(elf, date):
#  todayEnd = dt.datetime.combine(date, Elf.dayEnd)
#  timeAvailable = todayEnd - elf.available
#  timeAvailable = int(math.floor(timeAvailable.total_seconds() / 60.0))
#  return int(math.floor(timeAvailable*elf.prod))

def getBestDuration(elf, date, bigJob):
  todayEnd = dt.datetime.combine(date, Elf.dayEnd)
  timeAvailable = todayEnd - elf.available
  timeAvailable = int(math.floor(timeAvailable.total_seconds() / 60.0))
  desProd = desiredProd(bigJob)
  timeOptimal = 0
  if desProd > elf.prod:
    timeOptimal = min(timeAvailable, optJobLength(desProd, elf.prod))
    return int(math.floor(timeOptimal*elf.prod))
  else:
    return bigJob


def formatSolnRow(row):
  formatted = row
  formatted[2] = toDateString(row[2])
  return formatted

def minutesInJobRange(jobslist, minimum = 0, maximum = 50000):
  totalMins = 0
  mini = max(minimum, 0)
  maxi = min(maximum, len(jobslist))
  for i in range(mini, maxi):
    totalMins += i*len(jobslist[i])
  return totalMins

def jobsInJobRange(jobslist, minimum = 0, maximum = 50000):
  jobs = 0
  mini = max(minimum, 0)
  maxi = min(maximum, len(jobslist))
  for i in range(mini, maxi):
    jobs += len(jobslist[i])
  return jobs

def timeFromMin(prod):
  return int(math.ceil(math.log(4*prod)*60/math.log(1.02)))

def desiredProd(bigJobMins):
  return .25*(1.02**(bigJobMins/600.0))

def optJobLength(desiredProd, prod):
  desiredIncrease = desiredProd/prod
  optHours = math.log(desiredIncrease)/math.log(1.02)
#  print(desiredIncrease)
  #print(int(math.floor(optHours*60.0)))
  return int(math.ceil(optHours*60.0))

#Setup


if __name__ == '__main__':

#Job list setup
#Jobs should be in lists of identical duration.
  jobslist = []


# Elf list setup
  elves = []
  for i in range(WORKFORCE):
    elves.append(Elf(i + 1))


  with open(toyFile, 'rb') as f:
    toyReader = csv.reader(f)
    toyReader.next()

    print("Reading in toys list...")
    for toy in toyReader:
      addJobToList(jobslist, int(toy[0]), int(toy[2]))
    print("Done.")

    print("Minutes in jobs at least 151 long:")
    print(minutesInJobRange(jobslist, minimum = 151))
    print("Minutes in jobs at most 150 long:")
    print(minutesInJobRange(jobslist, maximum = 151))
    print("jobs at least 151 long:")
    print(jobsInJobRange(jobslist, minimum = 151))
    print("jobs at most 150 long:")
    print(jobsInJobRange(jobslist, maximum = 151))


    with open(solnFile, 'wb') as w:
      solnWriter = csv.writer(w)
      solnWriter.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])



      currentDate = START_DATE
      lastDateTime = REF_DT
      print("Assigning jobs starting at " + str(currentDate))
      yearJobs = 0
      totalJobs = 0

      while len(jobslist) > 0:

        if currentDate.day == 1:
          if currentDate.month == 1:
            print("Happy " + str(currentDate.year) + "!")
            print(str(yearJobs) + " jobs were started this year.")
            if yearJobs == 0:
              print("You should let less productive elves work overtime.")
              break
            yearJobs = 0
          print(currentDate.strftime("%B") + "...")
          print("Jobs done: " + str(totalJobs))
          print("Longest job left: " + str(len(jobslist)))

        dayAssignment = []
        for elf in elves:
          dayAssignment.extend(scheduleElfDay(elf, jobslist, currentDate))
        dayAssignment = sorted(dayAssignment, key=itemgetter(2))
        yearJobs += len(dayAssignment)
        totalJobs += len(dayAssignment)
        if len(dayAssignment) > 0:
          lastDateTime = dayAssignment[-1][2]
          for job in dayAssignment:
            solnWriter.writerow(formatSolnRow(job))
        currentDate = currentDate + dt.timedelta(days = 1)

      totalMins = int((lastDateTime - REF_DT).total_seconds() / 60)
      print("LastDateTime:")
      print(lastDateTime)
      print("Score:")
      print(totalMins * math.log(len(elves)))


  #time1 = dt.datetime(2014,1,1,10,0)
  #time2 = dt.datetime(2014,1,1,18,0)
  #addJobToList(jobslist, 1, 30)
  #addJobToList(jobslist, 2, 40)
  #addJobToList(jobslist, 3, 30)
  #addJobToList(jobslist, 4, 6094)
  #print(assignJobToElf(elves[0], 30, time1, jobslist))
  #print(assignJobToElf(elves[1], 30, time1, jobslist))
  #print(assignJobToElf(elves[2], 40, time1, jobslist))
  #print(assignJobToElf(elves[3], 6094, time2, jobslist))
  #print(elves[3].available.time() == dt.time(9,34))
  #print(jobslist)



