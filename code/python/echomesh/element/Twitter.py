from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element.Repeat import Repeat
from echomesh.element import Load
from echomesh.util import RemoveHashtags

from gittwit.twitter.Search import Search

DEFAULT_PRELOAD = 1

class Twitter(Repeat):
  def __init__(self, parent, description):
    super(Twitter, self).__init__(parent, description, name='Twitter')
    preload = description.get('preload', DEFAULT_PRELOAD)
    search = description['search']
    if not isinstance(search, list):
      search = [search]

    self.searches = [Search(s, self.callback, preload=preload) for s in search]
    self.handler = description.get('handler')
    if self.handler:
      self.handler = Load.make_one(self, self.handler)
    self.remove_hashtags = description.get('remove_hashtags', True)

  def loop_target(self, t):
    for s in self.searches:
      s.refresh()
    super(Twitter, self).loop_target(t)

  def callback(self, twitter):
    if self.handler:
      text = twitter['text']
      try:
        text = unicode(text, 'utf-8')
      except:
        try:
          text = unicode(text)
        except:
          return
      if self.remove_hashtags:
        text = RemoveHashtags.remove_hashtags(text)
      twitter['text'] = text
      self.handler.handle(twitter)

