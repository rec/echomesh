from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element.Repeat import Repeat
from echomesh.element import Load
from gittwit.twitter.Search import Search

DEFAULT_PRELOAD = 1

class Twitter(Repeat):
  def __init__(self, parent, description):
    super(Twitter, self).__init__(parent, description, name='Twitter')
    preload = description.get('preload', DEFAULT_PRELOAD)
    search = description['search']
    if not isinstance(search, list):
      search = [search]

    def callback(twitter):
      if self.handler:
        self.handler.handle(twitter)

    self.searches = [Search(s, callback, preload=preload) for s in search]
    self.handler = description.get('handler')
    if self.handler:
      self.handler = Load.make_one(self, self.handler)
    self.broadcast = description.get('broadcast', not self.handler)

  def loop_target(self, t):
    for s in self.searches:
      s.refresh()
    super(Twitter, self).loop_target(t)

