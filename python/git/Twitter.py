from __future__ import absolute_import, division, print_function, unicode_literals

import twitter

from util import Util

TWITTER_SIZE = 140

def get_api(auth):
  return twitter.Api(**auth.twitter)

def post_update(text, auth):
  get_api(auth).PostUpdate(Util.truncate(text, TWITTER_SIZE))
