from __future__ import absolute_import, division, print_function, unicode_literals

import twitter

from util import String

TWITTER_SIZE = 140

def get_api(auth, name):
  return twitter.Api(**auth['twitter'][name])

def post_update(name, text, auth):
  get_api(auth, name).PostUpdate(String.truncate(text, TWITTER_SIZE))
