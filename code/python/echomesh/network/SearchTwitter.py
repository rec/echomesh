from __future__ import absolute_import, division, print_function, unicode_literals

import HTMLParser
import Queue
import json
import urllib
import urllib2
import yaml

from echomesh.util.thread import TimeLoop

ROOT = 'http://search.twitter.com/search.json'
PARSER = HTMLParser.HTMLParser()

def get_image_url(image):
  try:
    short_image = image.replace('_normal.', '.')
    urllib2.urlopen(short_image)
    return short_image
  except:
    return image

def process_tweet(tweet):
  def get(name):
    res = tweet.get(name, '')
    return urllib.unquote(PARSER.unescape(res.encode('utf8')))

  return {'image': get_image_url(get('profile_image_url')),
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
    if self.max_id_str:
      keywords['since_id'] = self.max_id_str
    raw = urllib2.urlopen(ROOT, urllib.urlencode(keywords)).read().decode('utf8')
    result = json.loads(raw)
    self.max_id_str = result['max_id_str']
    for tweet in result['results'][:self.preload]:
      self.callback(process_tweet(tweet))

class Loop(TimeLoop.TimeLoop):
  def __init__(self, key, callback, interval=3, preload=1, name='SearchLoop',
               timeout=None):
    super(Loop, self).__init__(name=name, timeout=timeout, interval=interval)
    self.search = Search(key, callback, preload)

  def start(self):
    super(Loop, self).start()

  def _command(self, t):
    self.search.refresh()

