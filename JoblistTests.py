from testCode import *
from Joblist import *

def test_add():
  #Testing Joblist.add
  functName = 'Joblist.add'
  passed = True
  jobs = Joblist()

  #add to empty list
  jobs.add(1, 4)
  expectedOut = [[[],[],[],[],[1]], 1, 4]
  out = [jobs.l, jobs.length, jobs.minJobLength]
  passed = checkForError(functName, out, expectedOut) and passed

  #add before end of list
  jobs.add(2, 2)
  expectedOut = [[[],[],[2],[],[1]], 2, 2]
  out = [jobs.l, jobs.length, jobs.minJobLength]
  passed = checkForError(functName, out, expectedOut) and passed

  #add to beginning of list
  jobs.add(3, 1)
  expectedOut = [[[],[3],[2],[],[1]], 3, 1]
  out = [jobs.l, jobs.length, jobs.minJobLength]
  passed = checkForError(functName, out, expectedOut) and passed

  #add to end of list
  jobs.add(4, 4)
  expectedOut = [[[],[3],[2],[],[1,4]], 4, 1]
  out = [jobs.l, jobs.length, jobs.minJobLength]
  passed = checkForError(functName, out, expectedOut) and passed

  #add beyond end of list
  jobs.add(5, 7)
  expectedOut = [[[],[3],[2],[],[1,4],[],[],[5]], 5, 1]
  out = [jobs.l, jobs.length, jobs.minJobLength]
  passed = checkForError(functName, out, expectedOut) and passed

  #add to dur that is nonempty
  jobs.add(6, 4)
  expectedOut = [[[],[3],[2],[],[1,4,6],[],[],[5]], 6, 1]
  out = [jobs.l, jobs.length, jobs.minJobLength]
  passed = checkForError(functName, out, expectedOut) and passed

  #invalid ID
  jobs.add(-1,4)
  expectedOut = [[[],[3],[2],[],[1,4,6],[],[],[5]], 6, 1]
  out = [jobs.l, jobs.length, jobs.minJobLength]
  passed = checkForError(functName, out, expectedOut) and passed

  #invalid duration
  jobs.add(7,0)
  expectedOut = [[[],[3],[2],[],[1,4,6],[],[],[5]], 6, 1]
  out = [jobs.l, jobs.length, jobs.minJobLength]
  passed = checkForError(functName, out, expectedOut) and passed

  if passed:
    print(functName + ' has passed all tests.')


def test_get():
  functName = 'Joblist.get'
  passed = True
  jobs = Joblist()
  jobs.add(1, 4)
  jobs.add(2, 2) 
  jobs.add(3, 1)
  jobs.add(4, 4)
  jobs.add(5, 2)

  #check invalid duration
  out = [jobs.get(3), jobs.l, jobs.length, jobs.minJobLength]
  expectedOut = [False, [[],[3],[2,5],[],[1,4]], 5, 1]
  passed = checkForError(functName, out, expectedOut) and passed

  #check begin of list
  out = [jobs.get(1), jobs.l, jobs.length, jobs.minJobLength]
  expectedOut = [3, [[],[],[2,5],[],[1,4]], 4, 2]
  passed = checkForError(functName, out, expectedOut) and passed

  #check end of list (and mult. elts)
  out = [jobs.get(4), jobs.l, jobs.length, jobs.minJobLength]
  expectedOut = [1, [[],[],[2,5],[],[4]], 3, 2]
  passed = checkForError(functName, out, expectedOut) and passed

  #check middle of list
  out = [jobs.get(2), jobs.l, jobs.length, jobs.minJobLength]
  expectedOut = [2, [[],[],[5],[],[4]], 2, 2]
  passed = checkForError(functName, out, expectedOut) and passed

  #check make list shorter
  out = [jobs.get(4), jobs.l, jobs.length, jobs.minJobLength]
  expectedOut = [4, [[],[],[5]], 1, 2]
  passed = checkForError(functName, out, expectedOut) and passed

  #check remove last item from list
  out = [jobs.get(2), jobs.l, jobs.length, jobs.minJobLength]
  expectedOut = [5, [], 0, 0]
  passed = checkForError(functName, out, expectedOut) and passed

  if passed:
    print(functName + ' has passed all tests.')

def test_hasDuration():
  functName = 'Joblist.hasDuration'
  passed = True
  jobs = Joblist()
  jobs.add(1, 4)
  jobs.add(2, 2) 
  jobs.add(3, 1)
  jobs.add(4, 4)

  #check valid duration
  out = jobs.hasDuration(2)
  expectedOut = True
  passed = checkForError(functName, out, expectedOut) and passed

  #check duration less than zero
  out = jobs.hasDuration(-1)
  expectedOut = False
  passed = checkForError(functName, out, expectedOut) and passed  

  #check duration too long
  out = jobs.hasDuration(10)
  expectedOut = False
  passed = checkForError(functName, out, expectedOut) and passed  

  #check duration for which no jobs exist
  out = jobs.hasDuration(3)
  expectedOut = False
  passed = checkForError(functName, out, expectedOut) and passed  

  if passed:
    print(functName + ' has passed all tests.')



if __name__ == '__main__':

  test_add()
  test_get()
  test_hasDuration()

