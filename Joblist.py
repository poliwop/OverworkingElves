
class Joblist:
  def __init__(self):
    self.l = [[]]
    self.length = 0
    self.minJobLength = 0


  def add(self, ID, duration):
    """ Adds a job to the list.
    :param ID: int job ID
    :param duration: int length in minutes required to complete job
    """
    if ID > 0 and duration > 0:
      while len(self.l) <= duration:
        self.l.append([])
      self.l[duration].append(ID)
      self.length += 1
      self.updateMinJobAdd(duration)


  def getShortestDurIn(self, durList):
    durList.sort()
    return self.getFirstDurIn(durList)

  def getLongestDurIn(self, durList):
    durList.sort(reverse = True)
    return self.getFirstDurIn(durList)

  def getFirstDurIn(self, durList):
    for dur in durList:
      if self.hasDuration(dur):
        return dur
    return False


  def get(self, duration):
    """ Removes of specified duration from list, if one exists, returns
    ID. Otherwise, returns False.
    :param duration: int job duration
    :return: int job ID
    """
    job = False
    if self.hasDuration(duration):
      job = self.l[duration].pop(0)
      if self.l[duration] == []:
        self.shortenList()
        self.updateMinJobGet()
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
    return duration > 0 and duration < len(self.l) and self.l[duration] != []



  #Utility methods

  def updateMinJobAdd(self, dur):
    """Updates minJobLength when job is added to list."""
    if self.minJobLength > 0:
      self.minJobLength = min(self.minJobLength, dur)
    else:
      self.minJobLength = dur


  def updateMinJobGet(self):
    """Updates minJobLength when job is removed from list."""
    if len(self.l) > self.minJobLength:
      while self.l[self.minJobLength] == []:
        self.minJobLength += 1
    else:
      self.minJobLength = 0


  def shortenList(self):
    """Removes unneeded durations with no jobs from end of list."""
    while self.l != [] and self.l[-1] == []:
      self.l.pop()
