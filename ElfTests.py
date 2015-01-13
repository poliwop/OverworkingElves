'''
OverworkingElves: a solution to the Kaggle 2014 Christmas optimization competition.
Copyright 2014 Colin Grove. See README for more info.
'''

from testCode import *
from Elf import *


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


def test_adjustAvailability():

  functName = 'Elf.adjustAvailability'
  passed = True
  elf = Elf(1)

  #work for an hour in sanctioned time
  inpu = [60, 0, dt.datetime(2015, 1, 1, 9, 0)]
  expectedOut = dt.datetime(2015, 1, 1, 10, 0)
  elf.adjustAvailability(*inpu)
  out = elf.available
  passed = checkForError(functName, out, expectedOut) and passed
  
  #work for 30 minutes in unsanctioned time
  inpu = [0, 30, dt.datetime(2015, 1, 1, 20, 0)]
  expectedOut = dt.datetime(2015, 1, 2, 9, 30)
  elf.adjustAvailability(*inpu)
  out = elf.available
  passed = checkForError(functName, out, expectedOut) and passed

  #work for 3 hours of sanctioned time, 1 hour of unsanctioned time
  inpu = [3*60, 60, dt.datetime(2015, 1, 1, 16, 0)]
  expectedOut = dt.datetime(2015, 1, 2, 10, 0)
  elf.adjustAvailability(*inpu)
  out = elf.available
  passed = checkForError(functName, out, expectedOut) and passed

  #end at 5PM sharp
  inpu = [17, 0, dt.datetime(2015, 1, 1, 18, 43)]
  expectedOut = dt.datetime(2015, 1, 2, 9, 0)
  elf.adjustAvailability(*inpu)
  out = elf.available
  passed = checkForError(functName, out, expectedOut) and passed

  #work into next sanctioned time
  inpu = [3*60, 14*60, dt.datetime(2015, 1, 1, 18, 0)]
  expectedOut = dt.datetime(2015, 1, 3, 15, 0)
  elf.adjustAvailability(*inpu)
  out = elf.available
  passed = checkForError(functName, out, expectedOut) and passed

  #work 2 days
  inpu = [2*600, 2*840, dt.datetime(2015, 1, 1, 10, 0)]
  expectedOut = dt.datetime(2015, 1, 5, 18, 0)
  elf.adjustAvailability(*inpu)
  out = elf.available
  passed = checkForError(functName, out, expectedOut) and passed

  if passed:
    print(functName + ' has passed all tests.')


def test_workJob():

  functName = 'Elf.workJob'
  passed = True
  elf = Elf(1)

  #work for an hour in sanctioned time
  inpu = [60, dt.datetime(2015, 1, 1, 9, 0)]
  expectedOut = [dt.datetime(2015, 1, 1, 10, 0), 1.02]
  elf.workJob(*inpu)
  out = [elf.available, elf.prod]
  passed = checkForError(functName, out, expectedOut) and passed

  #Work for another hour: does jobTime go down appropriately?
  inpu = [60, dt.datetime(2015, 1, 1, 10, 0)]
  expectedOut = [dt.datetime(2015, 1, 1, 10, 59),
                 elf.prod*Elf.prodIncRate**(59/60.0)]
  elf.workJob(*inpu)
  out = [elf.available, elf.prod]
  passed = checkForError(functName, out, expectedOut) and passed

  #Work during bad hours
  inpu = [120, dt.datetime(2015, 1, 1, 18, 0)]
  expectedOut = [dt.datetime(2015, 1, 2, 9, 56),
                 elf.prod*Elf.prodIncRate**(60/60.0)
                         *Elf.prodDecRate**(56/60.0)]
  elf.workJob(*inpu)
  out = [elf.available, elf.prod]
  passed = checkForError(functName, out, expectedOut) and passed

  #Try to start too soon
  inpu = [60, dt.datetime(2015, 1, 2, 9, 0)]
  expectedOut = False
  out = elf.workJob(*inpu)
  passed = checkForError(functName, out, expectedOut) and passed



  if passed:
    print(functName + ' has passed all tests.')


if __name__ == '__main__':

  test_adjustProductivity()
  test_adjustAvailability()
  test_workJob()
