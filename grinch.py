from Joblist import *
from Elf import *
import numpy as np
import csv as csv
from operator import itemgetter

toyFile = 'data/toys_rev2.csv'
solnFile = 'soln/grinch003.csv'
WORKFORCE = 900
REF_DT = dt.datetime(2014,1,1,0,0)
START_DATE = dt.date(2014,12,11)
MAX_JOB_LEN = 49000

#JobsList methods



class JobAssigmentSimulator:

  def __init__(self, jobs, elves, wr):
    self.jobs = jobs
    self.elves = elves
    self.wr = wr
    self.assignments = []
    self.multMin = .98
    self.prodHoldDiv = .8418

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
      jobList = self.assignJobRampToElf(elf)
      self.assignments.extend(jobList)
      i += 1
      if i % 10000 == 0:
        self.printUpdate()

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
    
  def assignJobRampToElf(self, elf):
    elfAssigns = []
    bigJob = len(self.jobs.l) - 1
    elfAssigns.extend(self.phaseRampFullDay(elf))
    desiredProd = min(Elf.maxProd, bigJob / float(MAX_JOB_LEN))
    elfAssigns.extend(self.phaseRampToProd(elf, desiredProd))
    elfAssigns.extend(self.phaseHold(elf))
    elfAssigns.append(self.assignJobToElf(elf, bigJob, elf.available))
    return elfAssigns

  #Right now, this phase does NOT choose full days first, but rather .98 of
  #full days. This would not be difficult to fix.
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
      job = self.doLongestJobToday(elf, currentStart)
      currentStart = elf.available
      if job == []:
        tomorrow = currentStart + dt.timedelta(days = 1)
        currentStart = WorkHours.startOfDay(tomorrow)
      if job != []:
        jobList.append(job)
    return jobList

  def phaseHold(self, elf):
    jobList = []
    job = 0
    job = []
    currentStart = elf.available
    if currentStart != WorkHours.startOfDay(currentStart):
      tomorrow = currentStart + dt.timedelta(days = 1)
      currentStart = WorkHours.startOfDay(tomorrow)
    job = self.doLongestJobToday(elf, currentStart, self.prodHoldDiv)
    if job != []:
      jobList.append(job)
    return jobList


  def getNextElf(self):
    next = self.elves[0]
    for elf in self.elves[1:]:
      if elf.available < next.available:
        next = elf
    return next



  def fillDayWithJob(self, elf, startTime, maxDiv = 1, maxMult = 1):
    job = []
    timeLeft = WorkHours.timeLeftToday(startTime)
    restOfDayDur = timeLeft*elf.prod
    dur = int(math.floor(restOfDayDur*maxMult))
    restOfDayDurMax = int(math.floor(restOfDayDur/maxDiv))
    jobDur = self.jobs.getShortestDurIn(range(dur,restOfDayDurMax+1))
    if jobDur > 0:
      job = self.assignJobToElf(elf, jobDur, startTime)
    return job


  def doLongestJobToday(self, elf, startTime, maxDiv = 1):
    job = []
    timeLeft = WorkHours.timeLeftToday(startTime)
    maxDur = int(math.floor(timeLeft*elf.prod/maxDiv))
    jobDur = self.jobs.getLongestDurIn(range(0,maxDur + 1))
    if jobDur > 0:
      job = self.assignJobToElf(elf, jobDur, startTime)
    return job



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


