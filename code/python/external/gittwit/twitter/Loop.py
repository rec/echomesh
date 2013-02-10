from echomesh.util.thread.TimeLoop import TimeLoop
from gittwit.twitter.Search import Search

class Loop(TimeLoop):
  def __init__(self, search, callback, interval=2, preload=1, name='SearchLoop',
               timeout=None):
    super(Loop, self).__init__(name=name, timeout=timeout, interval=interval)
    self.search = Search(search, callback, preload)

  def loop_target(self, t):
    self.search.refresh()

