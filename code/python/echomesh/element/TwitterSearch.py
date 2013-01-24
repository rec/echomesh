from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Loop
from echomesh.element import Register
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

    def callback(twitter):
      pass
    self.searches = [Search(s, callback, preload=preload) for s in search]

  def callback(self, twitter):
    # How exactly do we send events to the system?  Or do we call something
    # on ourselves?
    pass

Register.register(TwitterSearch)
