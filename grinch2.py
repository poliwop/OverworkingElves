from Joblist import *
from Elf import *
#from ElfList import *
import numpy as np
import csv as csv
import random
from operator import itemgetter

toyFile = 'data/toys_rev2.csv'
solnFile = '/home/colin/Desktop/soln/grinch2_023.csv'
WORKFORCE = 900
REF_DT = dt.datetime(2014,1,1,0,0)
START_DATE = dt.date(2014,12,11)
MAX_JOB_LEN = 45000
NUMOFTOYS = 10000000


#JobsList methods



class JobAssigmentSimulator:

  def __init__(self, jobs, elves, wr):
    self.jobs = jobs
    self.elves = elves
    self.wr = wr
    #self.assignments = []
    self.multMin = .99
    self.prodHoldMult = 1.1879
    self.littleBigJobMaxMult = 1.0
    #self.littleBigJobMinMult = 1.0
    self.lastWorkingMinute = REF_DT



  def assignJobs(self):
    print(jobs.minLength, jobs.maxLength)
    print('Beginning Ramping Phase...')
    currentDate = self.rampPhase()
    print('Beginning Minimum Productivity Phase...')
    print('Min job length: ' + str(self.jobs.minLength))
    self.minProdPhase()
    lastMin = int((self.lastWorkingMinute - REF_DT).total_seconds()/60.0)
    return lastMin*math.log(WORKFORCE + 1)


## Ramp phase ##

  def rampPhase(self):
    today = self.getNextElf().available.date()
    while 4*jobs.maxLength > MAX_JOB_LEN and jobs.minLength <= 150:
      for elf in self.elves:
        self.assignElfDay(elf, today)
      today = today + dt.timedelta(days = 1)

      ## Status update to terminal ##
      if today.day == 1 and today.month == 1:
        print("Happy " + str(today.year) + "!")
        jobsDone = 10000000 - self.jobs.length
        print(str(jobsDone) + ' jobs done.')
#      if today.year >= 2016:
#        break
#      if today.year >= 2020:
#        break
#      break





## Min productivity phase ##

  def minProdPhase(self):
    today = self.getNextElf().available.date()
    while self.jobs.length > 0:
      for elf in self.elves:
        while elf.available < WorkHours.endOfDay(today) and self.jobs.length > 0:
          self.assignJobToElf(elf, jobs.minLength, elf.available)
      today = today + dt.timedelta(days = 1)
      if today.day == 1 and today.month == 1:
        print("Happy " + str(today.year) + "!")
        jobsDone = 10000000 - self.jobs.length
        print(str(jobsDone) + ' jobs done.')
#      if today.year >= 2020:
#        break


## Day assignments during ramping ##

  def assignElfDay(self, elf, today):
    startOfToday = WorkHours.startOfDay(today)
    startTime = max(startOfToday, elf.available)
    jobDone = True
    bestBigDur = self.bestBigJobDur(elf)

    #Try a couple things at the start of the day
    jobDone = self.fillDayWithJob(elf, startTime, 1, self.multMin)
    #Do little big job
    if startTime == startOfToday and bestBigDur != self.jobs.maxLength:
      jobDone = self.assignJobToElf(elf, bestBigDur, startTime)
    if jobDone:
      elf.doBigJob = False
      startTime = max(startTime, elf.available)
    else:
      elf.doBigJob = True
      jobDone = True

    #Loop to complete jobs throughout the day
    while startTime < WorkHours.endOfDay(today) and self.jobs.length > 0 and jobDone:
      jobDone = False

      if not(elf.doBigJob):
        jobDone = self.fillDayWithJob(elf, startTime, 1, self.multMin)
      if not(jobDone):
          #Prepare to do little big job tomorrow
        if bestBigDur != self.jobs.maxLength:
          jobDone = self.fillDayWithJob(elf, startTime, 1, 0)
        if jobDone:
          elf.doBigJob = True
        else:
          #Ramp to desired productivity
          desiredProd = min(Elf.maxProd, self.jobs.maxLength / float(MAX_JOB_LEN))
          desiredProd = max(desiredProd, Elf.minProd)
          if desiredProd > elf.prod:
            jobDone = self.doProdRaiseJob(elf, startTime, desiredProd)
          if jobDone:
            elf.doBigJob = True
          else:
            #Do big job
            if elf.doBigJob and bestBigDur == self.jobs.maxLength and desiredProd <= elf.prod:
              jobDone = self.assignJobToElf(elf, bestBigDur, startTime)
              elf.doBigJob = True
        startTime = max(startTime, elf.available)


## Various job choosing methods ##

  def fillDayWithJob(self, elf, startTime, maxMult = 1, minMult = 1):
    jobDone = False
    timeLeft = WorkHours.timeLeftToday(startTime)
    minTime = int(math.ceil(minMult*timeLeft))
    maxTime = int(math.floor(maxMult*timeLeft))

    minDurs = getListOfDursForTime(minTime,elf.prod)
    while minDurs == []:
      if minTime > maxTime:
        return jobDone
      minTime += 1
      minDurs = getListOfDursForTime(minTime, elf.prod)
    minDur = min(minDurs)

    maxDurs = getListOfDursForTime(maxTime,elf.prod)
    while maxDurs == []:
      if minTime > maxTime:
        return jobDone
      maxTime -= 1
      maxDurs = getListOfDursForTime(maxTime, elf.prod)
    maxDur = max(maxDurs)

    if maxDur >= minDur:
      jobDur = self.jobs.getLongestDurIn(minDur,maxDur)
      if jobDur > 0:
        jobDone = self.assignJobToElf(elf, jobDur, startTime)
    return jobDone

  def bestBigJobDur(self, elf):
    #Check if it's better to do biggest job or little big job
    #Return duration of biggest job or little big job accordingly
    bigJob = self.jobs.maxLength
    optDur = getOptimalProdDecayDur(elf.prod, 600, bigJob)
    desDur = int(math.floor(optDur*self.littleBigJobMaxMult))
    if not(checkGoodProdDecayDur(elf.prod, 600, bigJob, desDur)):
      return bigJob
    maxDur = int(math.ceil(5000*self.littleBigJobMaxMult))
    minDur = int(math.floor(600*elf.prod)) + 1
    littleBigDur = self.jobs.getShortestDurIn(desDur, maxDur)
    if checkGoodProdDecayDur(elf.prod, 600, bigJob, littleBigDur):
      return littleBigDur
    else:
      return bigJob

  def doProdRaiseJob(self, elf, startTime, dProd):
    jobDone = self.shortestJobToProd(elf, startTime, dProd)
    if not(jobDone):
      jobDone = self.fillDayWithJob(elf, startTime, 1, 0)
    return jobDone


  def shortestJobToProd(self, elf, startTime, dProd):
    jobDone = False
    timeLeft = WorkHours.timeLeftToday(startTime)
    restOfDayDur = int(math.floor(timeLeft*elf.prod))
    desWorkTime = self.getTimeToProd(elf.prod, dProd)
    durList = getListOfDursForTime(desWorkTime, elf.prod)
    minDur = int(math.ceil(desWorkTime*elf.prod))
    if durList != []:
      minDur = min(durList)
    if desWorkTime > timeLeft:
      jobDone = self.fillDayWithJob(elf, startTime, 1, 0)
    else:
      jobDur = self.jobs.getShortestDurIn(minDur, restOfDayDur)
      if jobDur > 0:
        jobDone = self.assignJobToElf(elf, jobDur, startTime)
    return jobDone

  def getTimeToProd(self, prod, dProd):
    return int(math.ceil(60*math.log(dProd/prod)/math.log(Elf.prodIncRate)))




## Job assignment ##

  def assignJobToElf(self, elf, duration, startTime):
    job = ()
    jobID = self.jobs.get(duration)
    if jobID > 0:
      realDur = int(math.ceil(duration/elf.prod))
      if elf.workJob(duration, startTime):
        job = (jobID, elf.ID, startTime, realDur)
        self.writeJob(job)
        self.updateLastMinute(startTime, realDur)
        return True
      else:
        self.jobs.add(jobID, duration)
    return False

  def updateLastMinute(self, startTime, realDur):
    jobEnd = startTime + dt.timedelta(minutes = realDur)
    self.lastWorkingMinute = max(self.lastWorkingMinute, jobEnd)

## Next available Elf ##

  def getNextElf(self):
    next = self.elves[0]
    for elf in self.elves[1:]:
      if elf.available < next.available:
        next = elf
    return next

## Output to file ##

  def writeJob(self, job):
    jobOut = job
#    jobOut = (job[0], job[1], toDateString(job[2]), job[3])
    self.wr.writerow(jobOut)




## Calculations ##

def getListOfDursForTime(time, prod):
  lessTimeDurMax = int(math.floor(prod*(time - 1)))
  timeDurMax = int(math.floor(prod*time))
  return range(lessTimeDurMax + 1, timeDurMax + 1)

def checkGoodProdDecayDur(C, T, L, S, d = 0):
  incExp = -T/60.0 - 10*d
  decExp = -S/(60.0*C) + T/60.0 + 10*d
  Lmult = 1 - Elf.prodIncRate**(incExp)*.9**(decExp)
  Smult = 1 - C/Elf.minProd
  return L*Lmult > S*Smult and 600 < S/C


def getOptimalProdDecayDur(C, T, L, mult = 1, d = 0):
  #C is the current producitivy, T the time left in workday,
  #L the length of the biggest job.
  firstNumer = (1 - C/Elf.minProd)*(Elf.prodIncRate**(T/60.0 + 10*d))*60*C
  firstDenom = L*math.log(.9)
  if firstNumer/firstDenom > 0:
    termTwo = 60*C*math.log(firstNumer/firstDenom)/math.log(.9)
    return int(math.ceil(C*T + 600*C*d - termTwo)*mult)
  else:
    return -1



def toDateString(daytime):
  """Reformats datetime into approriate datestring format for sumbssion."""
  dayStr = " ".join([str(daytime.year), str(daytime.month), str(daytime.day)])
  timeStr = " ".join([str(daytime.hour), str(daytime.minute)])
  return dayStr + " " + timeStr


if __name__ == '__main__':

  with open(toyFile, 'rb') as f:
    toyReader = csv.reader(f)
    toyReader.next()

    jobs = Joblist()
    elves = [None]*WORKFORCE
    firstAvail = WorkHours.startOfDay(START_DATE)
    for i in range(WORKFORCE):
      elves[i] = (Elf(i + 1, firstAvail))


    print("Reading in toys list...")
    for toy in toyReader:    
      jobs.add(int(toy[0]), int(toy[2]))
    print("Done.")



    '''
    ####   Testing code   ####
    print("Reading in toys list...")
    for i in range(10000):
      toy = toyReader.next()    
      jobs.add(int(toy[0]), int(toy[2]))
    print("Done.")
    ##########################
    '''
    

    with open(solnFile, 'wb') as w:
      solnWriter = csv.writer(w)
      solnWriter.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

      jobAssignSim = JobAssigmentSimulator(jobs, elves, solnWriter)
      score = jobAssignSim.assignJobs()
      print("Score: " + str(score))


