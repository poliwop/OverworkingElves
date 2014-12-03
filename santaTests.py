from santa import *

def testFunction(function, cases):
  passed = True
  for case in cases:
    [argList, output] = case
    result = function(*argList)
    if not(output == result):
      print "Case " + str(case) + " failed."
      print "[output, result]: " + str([output, result])
    passed = passed and (output == result)
  return passed


if __name__ == '__main__':

  print("Testing onMinToProd...")

  if testFunction(onMinToProd, onMinToProd_cases):
    print("Pass.")
  else:
    print("Fail.")

  print("Testing timeLeftToday...")
  
  if testFunction(timeLeftToday, timeLeftToday_cases):
    print("Pass.")
  else:
    print("Fail.")
