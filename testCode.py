'''
OverworkingElves: a solution to the Kaggle 2014 Christmas optimization competition.
Copyright 2014 Colin Grove. See README for more info.
'''

def testFunctionCases(function, cases, prec=7):
  passed = True
  errStr = ""
  for case in cases:
    [argList, output] = case
    result = function(*argList)
    if type(output) == type(1.0):
      output = round(output, prec)
      result = round(result, prec)
    if not(output == result):
      errStr = errStr + "\nCase " + str(case) + " failed."
      errStr = errStr + "\n[output, result]: " + str([output, result])
    passed = (passed and (output == result))
  return passed, errStr

def testFunction(function, cases):
  funName = function.__name__
  print("Testing " + funName + "...")
  testResult, errStr = testFunctionCases(function, cases)
  if testResult:
    print("Pass.")
  else:
    print("Fail.\n" + errStr)

def printTestError(functName, aOut, eOut):
  print('Test failed by ' + functName)
  print('Expected output: ' + str(eOut))
  print('Actual output: ' + str(aOut))

def checkForError(functName, aOut, eOut):
  passed = True
  if aOut != eOut:
    printTestError(functName, aOut, eOut)
    passed = False
  return passed
