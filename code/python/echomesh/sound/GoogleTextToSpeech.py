from __future__ import absolute_import, division, print_function, unicode_literals

import requests

from echomesh.util.file import Cache
from echomesh.util import Log

LOGGER = Log.logger(__name__)

URL = 'http://translate.google.com/translate_tts'
HEADERS = {'User-Agent': 'Mozilla'}
PARAMS = {'ie': 'UTF-8'}

def text_to_speech(text, tl='en'):
  """
  Given a phrase in a language that Google translate supports, returns a binary
  string representing an mp3 file, or raises an exception if this is impossible.

  """
  params = dict(PARAMS, q=text, tl=tl)
  LOGGER.vdebug('About to request url=%s, params=%s', URL, params)
  r = requests.get(URL, params=params, headers=HEADERS)
  if not r.ok:
    raise Exception("%d: couldn't read URL %s for '%s'" %
                    (r.status_code, r.url, text))

  return r.content

class TextToSpeechCache(Cache.Cache):
  def _get_file_contents(self, key):
    return text_to_speech(key)

CACHE = TextToSpeechCache(name='text-to-speech', suffix='.mp3')
