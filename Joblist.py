from collections import deque
#from first import first

class Joblist:
  def __init__(self):
    self.l = [deque()]
    self.length = 0
    self.minLength = 0
    self.maxLength = 0


  def add(self, ID, duration):
    """ Adds a job to the list.
    :param ID: int job ID
    :param duration: int length in minutes required to complete job
    """
    if ID > 0 and duration > 0:
      while len(self.l) <= duration:
        self.l.append(deque())
      self.l[duration].append(ID)
      self.length += 1
      self.updateMinJobAdd(duration)
      self.maxLength = max(duration, self.maxLength)

  '''
  def getShortestDurIn(self, durList):
    durList.sort()
    return self.getFirstDurIn(durList)

  def getLongestDurIn(self, durList):
    durList.sort(reverse = True)
    return self.getFirstDurIn(durList)
  '''

  def getLongestDurIn(self, mini, maxi):
    maxim = min(maxi, len(self.l) - 1)
    minim = max(mini, 1)
#    return first(range(maxim, minim - 1, -1), key = self.l.__getitem__,
#                 default = False)
    for dur in range(maxim, minim - 1, -1):
      if self.l[dur]:
        return dur
    return False

  def getShortestDurIn(self, mini, maxi):
    maxim = min(maxi, len(self.l) - 1)
    minim = max(mini, 1)
#    return first(range(minim, maxim + 1), key = self.l.__getitem__,
#                 default = False)
    for dur in range(minim, maxim + 1):
      if self.l[dur]:
        return dur
    return False

  '''
  def getLastDurIn(self, durList):
    for i in range(len(durList)):
      if self.hasDuration(durList[-i-1]):
        return durList[-i-1]
    return False

  def getFirstDurIn(self, durList):
    for dur in durList:
      if self.hasDuration(dur):
        return dur
    return False
  '''

  def get(self, duration):
    """ Removes of specified duration from list, if one exists, returns
    ID. Otherwise, returns False.
    :param duration: int job duration
    :return: int job ID
    """
    job = False
    if self.hasDuration(duration):
      job = self.l[duration].popleft()
      if len(self.l[duration]) == 0:
        self.shortenList()
        self.updateMinJobGet()
        self.maxLength = len(self.l) - 1
      self.length -= 1
    return job


  def hasDurIn(self, durList):
    has = False
    for dur in durList:
      has = has or self.hasDuration(dur)
    return has


  def hasDuration(self, duration):
    """:param duration: int duration
       :return: boolean indicating whether a job of the duration is in
                the list"""
    return duration > 0 and duration < len(self.l) and len(self.l[duration]) > 0



  #Utility methods

  def updateMinJobAdd(self, dur):
    """Updates minLength when job is added to list."""
    if self.minLength > 0:
      self.minLength = min(self.minLength, dur)
    else:
      self.minLength = dur


  def updateMinJobGet(self):
    """Updates minLength when job is removed from list."""
    if self.length == 0:
      self.minLength = 0
    else:
      while len(self.l) > self.minLength and len(self.l[self.minLength]) == 0:
        self.minLength += 1


  def shortenList(self):
    """Removes unneeded durations with no jobs from end of list."""
    while self.l != [] and len(self.l[-1]) == 0:
      self.l.pop()
