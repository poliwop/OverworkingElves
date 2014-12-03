from santa import *

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


if __name__ == '__main__':

  testFunction(onMinToProd, onMinToProd_cases)
  testFunction(timeLeftToday, timeLeftToday_cases)
  testFunction(desiredProd, desiredProd_cases)


