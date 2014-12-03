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
  caseList = []
  caseList.append([[dt.datetime(2014,1,1,9,5),dt.date(2014,1,1)],595])
  caseList.append([[dt.datetime(2014,1,1,14,0),dt.date(2014,1,1)],300])
  caseList.append([[dt.datetime(2014,2,2,9,0),dt.date(2014,2,2)],600])
  caseList.append([[dt.datetime(2014,2,2,19,0),dt.date(2014,2,2)],0])
  caseList.append([[dt.datetime(2014,2,2,19,21),dt.date(2014,2,2)],0])
  caseList.append([[dt.datetime(2014,2,2,8,20),dt.date(2014,2,2)],600])
  caseList.append([[dt.datetime(2014,2,3,10,0),dt.date(2014,2,2)],0])
  caseList.append([[dt.datetime(2014,2,2,10,0),dt.date(2014,2,3)],600])
  caseList.append([[dt.datetime(2014,2,2,21,0),dt.date(2014,2,3)],600])
  if testFunction(timeLeftToday, caseList):
    print("Pass.")
  else:
    print("Fail.")
