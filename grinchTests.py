from testCode import *
from grinch import *

#addJobToList(jobList, jobID, duration)
def addJobToList_cases():
  cases=[]
  inpu.append([[], 3, 4])
  outpu.append([
  cases.append([[[], 3, 4]

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


if __name__ == '__main__':

  
