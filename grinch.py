from Joblist import *
from Elf import *
import numpy as np
import csv as csv
import random
from operator import itemgetter

toyFile = 'data/toys_rev2.csv'
solnFile = 'soln/grinch019.csv'
WORKFORCE = 900
REF_DT = dt.datetime(2014,1,1,0,0)
START_DATE = dt.date(2014,12,11)
MAX_JOB_LEN = 44900

#JobsList methods



class JobAssigmentSimulator:

  def __init__(self, jobs, elves, wr):
    self.jobs = jobs
    self.elves = elves
    self.wr = wr
    self.assignments = []
    self.multMin = .99
    self.prodHoldMult = 1.1879

  def assignJobs(self):
    print('Beginning Ramping Phase...')
    self.rampPhase()
    print('Beginning Minimum Productivity Phase...')
    print('Min job length: ' + str(self.jobs.minJobLength))
    self.minProdPhase()
    self.assignments = [x for x in self.assignments if x != []]
    self.assignments = sorted(self.assignments, key=itemgetter(2))
    lastAssign = self.assignments[-1]
    lastMin = int((lastAssign[2] - REF_DT).total_seconds()/60.0)
    self.writeAssignments(self.assignments)
    return lastMin*math.log(WORKFORCE + 1)


  def rampPhase(self):
    bigJob = len(self.jobs.l) - 1
    i = 0
    while 4*bigJob > MAX_JOB_LEN:
      bigJob = len(self.jobs.l) - 1
      elf = self.getNextElf()
      #jobList = self.assignJobRampToElf(elf)
      jobList = self.assignVariableRampToElf(elf)
      self.assignments.extend(jobList)
      i += 1
      if i % 10000 == 0:
        self.printUpdate()
#      if i % 100000 == 0:
#        break
        

  def minProdPhase(self):
    currentDate = self.getNextElf().available
    while self.jobs.length > 0:
      for elf in self.elves:
        while elf.available < WorkHours.endOfDay(currentDate) and self.jobs.length > 0:
          bigJob = len(self.jobs.l) - 1
          job = self.assignJobToElf(elf, bigJob, elf.available)
          self.assignments.append(job)
      currentDate = currentDate + dt.timedelta(days = 1)
      if currentDate.day == 1 and currentDate.month == 1:
        print("Happy " + str(currentDate.year) + "!")
        jobsDone = 10000000 - self.jobs.length
        print(str(jobsDone) + ' jobs done.')


  def printUpdate(self):
    print('jobs done: ' + str(10000000 - self.jobs.length))

  def assignVariableRampToElf(self, elf):
    elfAssigns = []
    elfAssigns.extend(self.phaseRampFullDay(elf))
    elfAssigns.extend(self.phaseGetToBigJob(elf))
    
#    elfAssigns.extend(self.phaseAssignBigJob(elf))
    return elfAssigns

  def phaseGetToBigJob(self, elf):
    bigAssigned = False
    smallJobsLeft = True
    jobs = 0
    jobList = []
    bigJob = len(self.jobs.l) - 1
    while jobs != [[]] and not(bigAssigned) and self.jobs.length > 0:
      #Get duration for better big job. If prod level isn't high enough,
      #ramp up and then loop.
      jobs = [[]]
      bigJob = len(self.jobs.l) - 1
      bigJobDur = self.bestBigJobDur(elf)
      desiredProd = min(Elf.maxProd, bigJobDur / float(MAX_JOB_LEN))
      desiredProd = max(desiredProd, Elf.minProd)
      if desiredProd > elf.prod:
        jobs = [self.doProdRaiseJob(elf, elf.available, desiredProd)]
      elif bigJob != bigJobDur:
        jobs = self.doLittleBigJob(elf, bigJobDur)
        bigAssigned = True
      if jobs == [[]]:
        jobs = [self.assignJobToElf(elf, bigJob, elf.available)]
        bigAssigned = True
      jobList.extend(jobs)
    return jobList

  def bestBigJobDur(self, elf):
    #Check if it's better to do biggest job or little big job
    #Return duration of biggest job or little big job accordingly
    bigJob = len(self.jobs.l) - 1
    desDur = getOptimalProdDecayDur(elf.prod, 600, bigJob)
    littleBigDur = self.jobs.getShortestDurIn(range(desDur, bigJob + 1))
    if checkGoodProdDecayDur(elf.prod, 600, bigJob, littleBigDur):
      return littleBigDur
    else:
      return bigJob

  def doLittleBigJob(self, elf, dur):
    jobList = self.fillDayWithJobs(elf, elf.available)
    startTime = elf.available
    if startTime != WorkHours.startOfDay(startTime):
      tomorrow = currentStart + dt.timedelta(days = 1)
      startTime = WorkHours.startOfDay(tomorrow)
    job = self.assignJobToElf(elf, dur, startTime)
    if job != []:
      jobList.append(job)
    return jobList
  '''
  def isBestToDoBigJob(self, elf):
    bigJob = len(self.jobs.l) - 1
    desDur = getOptimalProdDecayDur(elf.prod, 600, bigJob)
    if checkGoodProdDecayDur(elf.prod, 600, bigJob, desDur):
      return False
    else:
      return True
  '''

  '''
  def phaseAssignBigJob(self, elf):
    bigAssigned = False
    smallJobsLeft = True
    job = 0
    jobList = []
    #  Loop until big job assigned: Get best big job dur
    #  If prod is not big enough to get under MaxTime, do little job
    #  and loop back.
    while job != [] and not(bigAssigned) and self.jobs.length > 0:
      bestBigDur = self.getBestBigJobDuration(elf)
      desiredProd = min(Elf.maxProd, bestBigDur / float(MAX_JOB_LEN))
      desiredProd = max(desiredProd, Elf.minProd)
      if desiredProd > elf.prod:
        job = self.doProdRaiseJob(elf, elf.available, desiredProd)
#        print('Raising productivity!')
      else:
        maxDur = len(self.jobs.l)
        jobDur = self.jobs.getShortestDurIn(range(bestBigDur, maxDur))
        job = self.assignJobToElf(elf, jobDur, elf.available)
        bigAssigned = True
#        print('Assigning big job!')
#        print('bestBigDur: ' + str(bestBigDur))
      if job != []:
        jobList.append(job)
    return jobList


  def getBestBigJobDuration(self, elf):
    bigJob = len(self.jobs.l) - 1
    timeLeft = WorkHours.timeLeftToday(elf.available)
    desDur = getOptimalProdDecayDur(elf.prod, timeLeft, bigJob)
    if checkGoodProdDecayDur(elf.prod, timeLeft, bigJob, desDur):
      return desDur
    else:
      return bigJob
  '''

  def doProdRaiseJob(self, elf, startTime, dProd, tryNextDay = True):
    job = self.shortestJobToProd(elf, startTime, dProd)
    if job == []:
      job = self.fillDayWithJob(elf, startTime, 1, 0)
      if job == [] and tryNextDay:
        tomorrow = startTime + dt.timedelta(days = 1)
        currentStart = WorkHours.startOfDay(tomorrow)
        job = self.doProdRaiseJob(elf, currentStart, dProd, False)
    return job
    
  def assignJobRampToElf(self, elf):
    elfAssigns = []
    bigJob = len(self.jobs.l) - 1
    elfAssigns.extend(self.phaseRampFullDay(elf))
    desiredProd = min(Elf.maxProd, bigJob / float(MAX_JOB_LEN))
    elfAssigns.extend(self.phaseRampToProd(elf, desiredProd))
    elfAssigns.extend(self.phaseDecay(elf, bigJob))
#    elfAssigns.extend(self.phaseHold(elf))
    elfAssigns.append(self.assignJobToElf(elf, bigJob, elf.available))
    return elfAssigns


  def phaseRampFullDay(self, elf):
    jobList = []
    job = 0
    currentStart = elf.available
    while elf.prod < 4.0 and job != []:
      job = []
      job = self.fillDayWithJob(elf, currentStart, 1, self.multMin)
      currentStart = elf.available
      if job != []:
        jobList.append(job)
        tomorrow = currentStart + dt.timedelta(days = 1)
        currentStart = WorkHours.startOfDay(tomorrow)
    return jobList

  def phaseRampToProd(self, elf, dProd):
    jobList = []
    job = []
    currentStart = elf.available
    while elf.prod < dProd and self.jobs.minJobLength <= 600*elf.prod:
      job = self.shortestJobToProd(elf, currentStart, dProd)
      if job == []:
        job = self.fillDayWithJob(elf, currentStart, 1, 0)
      currentStart = elf.available
      if job == []:
        tomorrow = currentStart + dt.timedelta(days = 1)
        currentStart = WorkHours.startOfDay(tomorrow)
      if job != []:
        jobList.append(job)
    return jobList

  def phaseDecay(self, elf, bigJob):
    jobList = []
    job = 0
    startProd = elf.prod
    while job != []:
      job = []
      timeLeft = WorkHours.timeLeftToday(elf.available)
      desDur = getOptimalProdDecayDur(elf.prod, timeLeft, bigJob)
      if desDur > startProd*600:
        maxDur = int(math.ceil(desDur*1.2))
        jobDur = self.jobs.getShortestDurIn(range(desDur, maxDur))
        if jobDur > 0:
          job = self.assignJobToElf(elf, jobDur, elf.available)
        if job != []:
          jobList.append(job)
    return jobList

  def phaseHold(self, elf):
    jobList = []
    job = []
    currentStart = elf.available
    if currentStart != WorkHours.startOfDay(currentStart):
      tomorrow = currentStart + dt.timedelta(days = 1)
      currentStart = WorkHours.startOfDay(tomorrow)
    job = self.fillDayWithJob(elf, currentStart, self.prodHoldMult)
    if job != []:
      jobList.append(job)
    return jobList


  def getNextElf(self):
    next = self.elves[0]
    for elf in self.elves[1:]:
      if elf.available < next.available:
        next = elf
    return next

  def getRandomElf(self):
    return random.choice(elves)


  def fillDayWithJobs(self, elf, startTime):
    jobList = []
    job = 0
    while job != [] and elf.available.date() == startTime.date():
      job = self.fillDayWithJob(elf, elf.available, 1, 0)
      if job != []:
        jobList.append(job)
    return jobList
      



  def fillDayWithJob(self, elf, startTime, maxMult = 1, minMult = 1):
    job = []
    timeLeft = WorkHours.timeLeftToday(startTime)
    restOfDayDur = timeLeft*elf.prod
    dur = int(math.floor(restOfDayDur*minMult))
    restOfDayDurMax = int(math.floor(restOfDayDur*maxMult))
    jobDur = self.jobs.getLongestDurIn(range(dur,restOfDayDurMax+1))
    if jobDur > 0:
      job = self.assignJobToElf(elf, jobDur, startTime)
    return job

  def shortestJobToProd(self, elf, startTime, dProd):
    job = []
    timeLeft = WorkHours.timeLeftToday(startTime)
    restOfDayDur = int(math.floor(timeLeft*elf.prod))
    desWorkTime = self.getTimeToProd(elf.prod, dProd)
    dur = int(math.ceil(desWorkTime*elf.prod))
    if dur > restOfDayDur:
      job = self.fillDayWithJob(elf, startTime, 1, 0)
    else:
      jobDur = self.jobs.getShortestDurIn(range(dur, restOfDayDur + 1))
      if jobDur > 0:
        job = self.assignJobToElf(elf, jobDur, startTime)
    return job

  def getTimeToProd(self, prod, dProd):
    return int(math.ceil(60*math.log(dProd/prod)/math.log(Elf.prodIncRate)))




  '''
  def doLongestJobToday(self, elf, startTime, maxDiv = 1):
    job = []
    timeLeft = WorkHours.timeLeftToday(startTime)
    maxDur = int(math.floor(timeLeft*elf.prod/maxDiv))
    jobDur = self.jobs.getLongestDurIn(range(0,maxDur + 1))
    if jobDur > 0:
      job = self.assignJobToElf(elf, jobDur, startTime)
    return job
  '''


  def assignJobToElf(self, elf, duration, startTime):
    job = []
    jobID = self.jobs.get(duration)
    if jobID > 0:
      realDur = int(math.ceil(duration/elf.prod))
      if elf.workJob(duration, startTime):
        job = [jobID, elf.ID, startTime, realDur]
      else:
        self.jobs.add(jobID, duration)
    return job


  # IO methods

  def writeAssignments(self, assignmentList):
    for job in assignmentList:
      job[2] = toDateString(job[2])
      self.wr.writerow(job)

def checkGoodProdDecayDur(C, T, L, S, d = 0):
  incExp = -T/60.0 - 10*d
  decExp = -S/(60.0*C) + T/60.0 + 10*d
  Lmult = 1 - Elf.prodIncRate**(incExp)*.9**(decExp)
  Smult = 1 - C/Elf.minProd
  return L*Lmult > S*Smult and 600 < S/C


def getOptimalProdDecayDur(C, T, L, d = 0):
  #C is the current producitivy, T the time left in workday,
  #L the length of the biggest job.
  firstNumer = (1 - C/Elf.minProd)*(Elf.prodIncRate**(T/60.0 + 10*d))*60*C
  firstDenom = L*math.log(.9)
  if firstNumer/firstDenom > 0:
    termTwo = 60*C*math.log(firstNumer/firstDenom)/math.log(.9)
    return int(math.ceil(C*T + 600*C*d - termTwo))
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
    elves = []
    firstAvail = WorkHours.startOfDay(START_DATE)
    for i in range(WORKFORCE):
      elves.append(Elf(i + 1, firstAvail))


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


