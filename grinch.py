from Joblist import *
from Elf import *
import numpy as np
import csv as csv
from operator import itemgetter

toyFile = 'data/toys_rev2.csv'
solnFile = 'soln/submission004.csv'
WORKFORCE = 900
REF_DT = dt.datetime(2014,1,1,0,0)
START_DATE = dt.date(2014,12,11)
TARGET_JOB_LEN = 46300

#JobsList methods





class JobAssigmentSimulator:

  def __init__(self, jobs, elves, wr):
    self.jobs = jobs
    self.elves = elves
    self.wr = wr

  def assignJobs(self):
    elf = self.elves[0]
    while jobs.length > 9500:
      bj = len(self.jobs.l) - 1
      job = self.assignJobToElf(elf,bj,elf.available)
      if job != []:
        self.writeAssignments([job])



  def assignJobToElf(self, elf, duration, startTime):
    job = []
    jobID = self.jobs.get(duration)
    if jobID > 0:
      realDur = int(math.ceil(duration/elf.prod))
      elf.workJob(duration, startTime)
      job = [jobID, elf.ID, startTime, realDur]
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
      elves.append(Elf(i, firstAvail))

    '''
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

    

    with open(solnFile, 'wb') as w:
      solnWriter = csv.writer(w)
      solnWriter.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

      jobAssignSim = JobAssigmentSimulator(jobs, elves, solnWriter)
      jobAssignSim.assignJobs()


