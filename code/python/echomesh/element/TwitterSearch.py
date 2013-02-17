from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element import Load
from echomesh.element import Loop
from gittwit.twitter.Search import Search

DEFAULT_INTERVAL = 10.0
DEFAULT_PRELOAD = 1

class TwitterSearch(Loop.Loop):
  def __init__(self, parent, description):
    interval = description.get('interval', DEFAULT_INTERVAL)
    super(TwitterSearch, self).__init__(parent, description, interval=interval)
    preload = description.get('preload', DEFAULT_PRELOAD)
    search = description['search']
    if not isinstance(search, list):
      search = [search]

    self.searches = [Search(s, self.callback, preload=preload) for s in search]
    self.handler = description.get('handler')
    if self.handler:
      self.handler = Load.make_one(self, self.handler)
    self.broadcast = description.get('broadcast', not self.handler)

  def callback(self, twitter):
    if self.handler:
      self.handler.handle(twitter)

  def loop_target(self, t):
    print('TwitterSearch: here!')
    for s in self.searches:
      s.refresh()

Element.register(TwitterSearch)
