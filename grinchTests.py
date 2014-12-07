from testCode import *
from grinch import *


toyFile = 'data/toys_rev2.csv'
solnFile = 'soln/test.csv'
WORKFORCE = 900
REF_DT = dt.datetime(2014,1,1,0,0)
START_DATE = dt.date(2014,12,11)
TARGET_JOB_LEN = 46300


def test_toDateString():
  cases = []

  cases.append([[dt.datetime(2015,1,1,9,0)],'2015 1 1 9 0'])
  cases.append([[dt.datetime(2015,1,3,9,17)],'2015 1 3 9 17'])

  testFunction(toDateString, cases)

if __name__ == '__main__':

#  test_toDateString()
  with open(toyFile, 'rb') as f:
    toyReader = csv.reader(f)
    toyReader.next()

    jobs = Joblist()
    elves = []
    for i in range(WORKFORCE):
      elves.append(Elf(i))

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


