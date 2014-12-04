
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
SANC_PROD_CHANGE = 1.02
UNSANC_PROD_CHANGE = .9
JOB_RATIO = 100.0


### New, Tested Methods ###



def scheduleElfDay(elf, day, jobsList):
  elfJobs = []
  bigJob = len(jobsList) - 1
  smallJobs = True
  while (elf.available.date() <= day) and smallJobs and jobsList != []:
    startTime = startTimeToday(elf.available, day)
    if bigJob > 2400 and elf.prod >= desiredProd(bigJob):
      job = assignJobToElf(elf, bigJob, startTime, jobsList)
      elfJobs.append(job)
    else:
      timeLeft = timeLeftToday(elf.available, day)
      smallJobs, duration = calcDurFromMaxDur(elf, timeLeft, jobsList)
      if smallJobs:
        job = assignJobToElf(elf, duration, startTime, jobsList)
        elfJobs.append(job)
  return elfJobs

def startTimeToday(availTime, day):
  if availTime.date() >= day:
    return availTime
  else:
    return dt.datetime.combine(day, Elf.dayStart)

'''
def calcSmallDuration(elf, day, jobsList):
#  jobAssigned = False
  bigJob = len(jobsList) - 1
  prodTarget = onMinToProd(elf.prod, desiredProd(bigJob))
  timeLeft = timeLeftToday(elf.available, day)
  maxDur = min(prodTarget, timeLeft)
  if prodTarget < timeLeft:
    duration = calcDurFromMaxDur(elf, prodTarget, jobslist)
    
#    jobAssigned, job = assignJobMaxDur(elf, prodTarget, startTime, jobsList)
#    if jobAssigned:
#      return True, job
  return assignJobMaxDur(elf, timeLeft, startTime, jobsList)
'''

def calcDurFromMaxDur(elf, maxDur, jobsList):
  duration = int(math.floor(maxDur*elf.prod))
  duration = min(duration, len(jobsList) - 1)
  while duration > 0 and jobsList[duration] == []:
    duration -= 1
  if duration == 0:
    return False, 0
  else:
    return True, duration

#Testing code
'''
def assignJobMaxDur_cases():
  cases=[]
  elf = Elf(1, dt.datetime(2015,1,1,9,0))
  jobsList = [[],[],[],[],[],[1,2,3],[],[],[4,5],[],[],[],[],[],[6]]
  inpu = []
  outpu = []
  inpu.append([elf, 10, 
'''

def assignJobToElf(elf, duration, startTime, jobsList):
  jobID = getJobFromList(jobsList, duration)[1]
  realDur = int(math.ceil(duration/elf.prod))
  elf.workJob(duration, startTime)
  return [jobID, elf.ID, startTime, realDur]


def getJobFromList(jobsList, duration):
  """ Takes the list of assignable jobs and a duration, selects
  a job of required duration and removes it from the list, returning
  the jobID.
  :param jobsList: list of jobs to be assigned
  :param duration: list of duration desired
  :return: list of jobs with job removed, jobID or False
  """
  if duration >= 0 and len(jobsList) > duration and len(jobsList[duration]) > 0:
    jobID = jobsList[duration].pop(0)
    while len(jobsList) > 0 and len(jobsList[-1]) == 0:
      jobsList.pop()
    return [jobsList, jobID]
  else:
    return [jobsList, False]

#Testing code
def getJobFromList_cases():
  cases=[]
  jobs = []
  durs = []
  outs = []
  jobs.append([[],[3,8,13498],[],[4,6,8,326,179],[],[],[],[1]])
  durs.append(3)
  outs.append([[[],[3,8,13498],[],[6,8,326,179],[],[],[],[1]],4]) 

  jobs.append([[],[3,8,13498],[],[4,6,8,326,179],[],[],[],[1]])
  durs.append(7)
  outs.append([[[],[3,8,13498],[],[4,6,8,326,179]], 1])

  jobs.append([[],[3,8,13498],[],[4,6,8,326,179],[],[],[],[1]])
  durs.append(6)
  outs.append([[[],[3,8,13498],[],[4,6,8,326,179],[],[],[],[1]], False])

  jobs.append([[],[3],[],[4,6,8,326,179],[],[],[],[17,65]])
  durs.append(7)
  outs.append([[[],[3],[],[4,6,8,326,179],[],[],[],[65]], 17])

  jobs.append([[],[],[3]])
  durs.append(2)
  outs.append([[], 3])

  jobs.append([[],[],[3]])
  durs.append(0)
  outs.append([[[], [], [3]], False])
  
  for i in range(len(jobs)):
    cases.append([[jobs[i],durs[i]], outs[i]])

  return cases



def desiredProd(bigJob):
  """
  :param bigJob: int length in minutes of big job
  :return: float productivity level which ensures performing
           big job will approx. maintain the job ratio
  """
  dProd = Elf.maxProd
  if JOB_RATIO > 0:
    dProd = Elf.minProd*(SANC_PROD_CHANGE)**(bigJob/(60.0*JOB_RATIO))
  return min(Elf.maxProd, dProd)

#Testing code
#Must change if JOB_RATIO or SANC_PROD_CHANGE change
def desiredProd_cases():
  cases=[]
  cases.append([[50000],.294854735])
  cases.append([[47470],.292402917])
  cases.append([[30001],.276021118])
  cases.append([[2001],.251656508])
  cases.append([[600],.250495556])
  cases.append([[150],.250123797])
  cases.append([[50],.250041259])
  return cases

def timeLeftToday(available, day):
  """
  :param available: datetime earliest availability of elf
  :param day: date current assignment day
  :return: int sanctioned time left
  """
  timeLeft = 0
  dayStartToday = dt.datetime.combine(day, Elf.dayStart)
  dayEndToday = dt.datetime.combine(day, Elf.dayEnd)
  if available.date() <= day:
    startTimeToday = dayStartToday
    if available.date() == day:
      startTimeToday = min(available, dayEndToday)
      startTimeToday = max(startTimeToday, dayStartToday)
    timeLeft = (dayEndToday - startTimeToday).total_seconds()/60.0
    timeLeft = int(math.floor(timeLeft))
  return timeLeft

#Testing code
def timeLeftToday_cases():
  cases = []
  cases.append([[dt.datetime(2014,1,1,9,5),dt.date(2014,1,1)],595])
  cases.append([[dt.datetime(2014,1,1,14,0),dt.date(2014,1,1)],300])
  cases.append([[dt.datetime(2014,2,2,9,0),dt.date(2014,2,2)],600])
  cases.append([[dt.datetime(2014,2,2,19,0),dt.date(2014,2,2)],0])
  cases.append([[dt.datetime(2014,2,2,19,21),dt.date(2014,2,2)],0])
  cases.append([[dt.datetime(2014,2,2,8,20),dt.date(2014,2,2)],600])
  cases.append([[dt.datetime(2014,2,3,10,0),dt.date(2014,2,2)],0])
  cases.append([[dt.datetime(2014,2,2,10,0),dt.date(2014,2,3)],600])
  cases.append([[dt.datetime(2014,2,2,21,0),dt.date(2014,2,3)],600])
  return cases




def onMinToProd(startProd, endProd):
  """
  :param startProd: float starting productivity level
  :param endProd: float ending productivity level
  :return: int number of sactioned minutes to go from startProd to endProd
  """
  startProd = float(startProd)
  endProd = float(endProd)
  onMinToProd = 60*math.log(endProd/startProd)/math.log(SANC_PROD_CHANGE)
  return int(math.ceil(onMinToProd))

#Testing code
#Must change if SANC_PROD_CHANGE changes
def onMinToProd_cases():
  return [[[3,3],0], [[5,6],553], [[.25,4.0],8401], [[.5,1],2101], 
          [[.37,2.2],5402], [[1,5],4877], [[.1,2],9077]]





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



'''

def scheduleElfDay(elf, jobs, date):
  elfJobs = []
  bigJob = len(jobs) - 1
  if elf.available.date() < date:
    elf.available = elf.startOfDay(date)
  if elf.available < elf.endOfDay(date):

    if bigJob > 150 and timeFromMin(elf.prod)*10 >= bigJob:
      job = assignJobToElf(elf, bigJob, elf.available, jobs)
      elfJobs.append(job)

    else:

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
'''

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

def getShortestJob(jobsList):
  dur = 0
  while jobsList[dur] == []:
    dur += 1
  return dur

'''
THIS FUNCTION HAS BEEN REPLACED
def desiredProd(bigJobMins):
  return .25*(1.02**(bigJobMins/600.0))


def optJobLength(desiredProd, prod):
  desiredIncrease = desiredProd/prod
  optHours = math.log(desiredIncrease)/math.log(1.02)
#  print(desiredIncrease)
  #print(int(math.floor(optHours*60.0)))
  return int(math.ceil(optHours*60.0))
'''


#Setup


if __name__ == '__main__':

#Job list setup
#Jobs should be in lists of identical duration.
  jobslist = []


# Elf list setup
  elves = []
  for i in range(WORKFORCE):
    elves.append(Elf(i + 1, dt.datetime(2014,12,11,9,0)))


  with open(toyFile, 'rb') as f:
    toyReader = csv.reader(f)
    toyReader.next()

    print("Reading in toys list...")
    for toy in toyReader:
      addJobToList(jobslist, int(toy[0]), int(toy[2]))
    print("Done.")

    print("Minutes in jobs at least 2401 long:")
    bigMins = minutesInJobRange(jobslist, minimum = 2401)
    print(bigMins)
    print("Minutes in jobs at most 2400 long:")
    smallMins = minutesInJobRange(jobslist, maximum = 2401)
    print(smallMins)
    JOB_RATIO = float(bigMins)/(smallMins*.95)

    print("jobs at least 2401 long:")
    print(jobsInJobRange(jobslist, minimum = 2401))
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
#      while len(jobslist) > 0 and currentDate < dt.date(2020,1,1):
        if currentDate.day == 1:
          if currentDate.month == 1:
            print("Happy " + str(currentDate.year) + "!")
            print(str(yearJobs) + " jobs were started this year.")
            if yearJobs == 0:
              print("You should let less productive elves work overtime.")
              break
            yearJobs = 0
            print("Jobs done: " + str(totalJobs))
            print("Longest job left: " + str(len(jobslist) - 1))
            print("Shortest job left: " + str(getShortestJob(jobslist)))
            print("Minutes in jobs at least 2401 long:")
            bigMins = minutesInJobRange(jobslist, minimum = 2401)
            print(bigMins)
            print("Minutes in jobs at most 150 long:")
            smallMins = minutesInJobRange(jobslist, maximum = 151)
            print(smallMins)
            JOB_RATIO = float(bigMins)/(smallMins)
#          print(currentDate.strftime("%B") + "...")


        dayAssignment = []
        for elf in elves:
          dayAssignment.extend(scheduleElfDay(elf, currentDate, jobslist))
        dayAssignment = sorted(dayAssignment, key=itemgetter(2))
        yearJobs += len(dayAssignment)
        totalJobs += len(dayAssignment)
        if len(dayAssignment) > 0:
          lastDateTime = dayAssignment[-1][2]
          for job in dayAssignment:
            if not(job == []):
              solnWriter.writerow(formatSolnRow(job))
        currentDate = currentDate + dt.timedelta(days = 1)

      totalMins = int((lastDateTime - REF_DT).total_seconds() / 60)
      print("LastDateTime:")
      print(lastDateTime)
      print("Score:")
      print(totalMins * math.log(len(elves) + 1))


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



