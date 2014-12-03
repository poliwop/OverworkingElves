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
  caseList = [[[3,3],0], [[5,6],553], [[.25,4.0],8401], [[.5,1],2101],
              [[.37,2.2],5402], [[1,5],4877], [[.1,2],9077]]
  if testFunction(onMinToProd, caseList):
    print("Pass.")
  else:
    print("Fail.")

  print("Testing timeLeftToday...")
  
  if testFunction(timeLeftToday, timeLeftToday_cases):
    print("Pass.")
  else:
    print("Fail.")
