from testCode import *
from Elf import *
from WorkHours import *
import math

def test_adjustProductivity():
  functName = 'Elf.adjustProductivity'
  passed = True
  elf = Elf(1)
 
  #work for an hour in sanctioned time
  expectedOut = elf.prod*(Elf.prodIncRate**1.0)
  elf.adjustProductivity(60, 0)
  out = elf.prod
  passed = checkForError(functName, out, expectedOut) and passed
  
  #work for 30 minutes in unsanctioned time
  expectedOut = elf.prod*(Elf.prodDecRate**.5)
  elf.adjustProductivity(0, 30)
  out = elf.prod
  passed = checkForError(functName, out, expectedOut) and passed

  #work for 3 hours of sanctioned time, 1 hour of unsanctioned time
  expectedOut = elf.prod*(Elf.prodIncRate**3.0)*(Elf.prodDecRate**1.0)
  elf.adjustProductivity(180, 60)
  out = elf.prod
  passed = checkForError(functName, out, expectedOut) and passed

  #work beyond max productivity
  expectedOut = 4.0
  elf.adjustProductivity(80*60, 0)
  out = elf.prod
  passed = checkForError(functName, out, expectedOut) and passed

  #work beyond min productivity
  expectedOut = .25
  elf.adjustProductivity(0, 30*60)
  out = elf.prod
  passed = checkForError(functName, out, expectedOut) and passed

  if passed:
    print(functName + ' has passed all tests.')



if __name__ == '__main__':

  test_adjustProductivity()
