from santa import *

def testFunctionCases(function, cases):
  passed = True
  errStr = ""
  for case in cases:
    [argList, output] = case
    result = function(*argList)
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

if __name__ == '__main__':

  testFunction(onMinToProd, onMinToProd_cases)
  testFunction(timeLeftToday, timeLeftToday_cases)


