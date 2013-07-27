from __future__ import absolute_import, division, print_function, unicode_literals

import twitter

from echomesh.base import Name
from echomesh.util.string import Truncate

TWITTER_SIZE = 140

def get_api(auth, name=''):
  return twitter.Api(**auth['twitter'][name or Name.NAME])

def post_update(text, auth, *names):
  text = Truncate.truncate(text, TWITTER_SIZE)
  for name in names:
    get_api(auth, name).PostUpdate(text)
  return text
