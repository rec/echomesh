from __future__ import absolute_import, division, print_function, unicode_literals

import HTMLParser
import Queue
import json
import urllib
import urllib2

from echomesh.util import Log

LOGGER = Log.logger(__name__)

ROOT = 'http://search.twitter.com/search.json'
PARSER = HTMLParser.HTMLParser()

def json_to_tweet(tweet):
  def get(name):
    return urllib.unquote(PARSER.unescape(tweet.get(name, '')))

  image_url = get('profile_image_url')
  try:
    short_url = image_url.replace('_normal.', '.')
    urllib2.urlopen(short_url)
    image_url = short_url
  except:
    pass

  return {'image_url': image_url,
          'text': get('text'),
          'user': get('from_user'),
          'user_name': get('from_user_name'),
          }

class Search(object):
  def __init__(self, key, callback, preload=1):
    self.key = key
    self.preload = preload
    self.queue = Queue.Queue()
    self.callback = callback
    self.max_id_str = ''

  def refresh(self):
    keywords = {'q': self.key}
    first_time = not self.max_id_str
    if not first_time:
      keywords['since_id'] = self.max_id_str
    raw = urllib2.urlopen(ROOT, urllib.urlencode(keywords)).read().decode('utf8')
    result = json.loads(raw)
    self.max_id_str = result['max_id_str']
    tweets = result['results']
    if first_time:
      tweets = tweets[:self.preload]
    for tweet in tweets:
      self.callback(json_to_tweet(tweet))

