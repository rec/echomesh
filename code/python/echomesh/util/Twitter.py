from __future__ import absolute_import, division, print_function, unicode_literals

import json
import twitter
import urllib

from echomesh.base import CommandFile
from echomesh.util.string import Truncate

TWITTER_SIZE = 140

API = None

def _get_api():
  global API
  if not API:
    auth = CommandFile.resolve('auth.py')
    API = auth and twitter.Api(**auth['twitter'])
  return API

def post_update(text, *names):
  text = Truncate.truncate(text, TWITTER_SIZE)
  for name in names:
    _get_api().PostUpdate(text)
  return text

class Search(object):
  def __init__(self, term, callback, preload=1, **kwds):
    _get_api()

    kwds['term'] = term
    self.kwds = kwds
    self.callback = callback
    self.preload = preload
    self.max_id = None

  def refresh(self):
    first_time = not self.max_id
    if first_time:
      results = API.GetSearch(**kwds)
    else:
      results = API.GetSearch(since_id=self.max_id, **kwds)

    if first_time and len(results) > self.preload:
      results = results[len(results) - self.preload:]

    for status in results:
      self.max_id = max(self.max_id, status.id)
      self.callback(status.AsDict())

