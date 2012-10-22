from __future__ import absolute_import, division, print_function, unicode_literals

# This is fairly specific to using a Yourls server:  see http://yourls.org/

import urllib
import urllib2

from util import Util
from util import Log

LOGGER = Log.logger(__name__)

SHORTEN_PART = 'yourls-api.php'

def _get_index(config, auth):
  if config['shorten']['use_index_url']:
    try:
      index_url = auth['index_url']
      return urllib2.urlopen(index_url).read().strip()
    except:
      LOGGER.error("Couldn't open shortener url %s", index_url)
      raise

  else:
    return Util.get_and_increment_index_file(config['shorten']['index_file'])


def shorten(url, config, auth):
  def _shortener_url(part):
    return '%s/%s' % (config['shorten']['url'], part)

  index = _get_index(config, auth)
  shorturl = config['shorten']['prefix'] + index
  data = urllib.urlencode(dict(signature=auth['yourls'],
                               action='shorturl',
                               keyword=shorturl,
                               url=url))
  resulting_url = _shortener_url(SHORTEN_PART)
  try:
    urllib2.urlopen(resulting_url, data)
  except:
    LOGGER.error("Shortener api failed on %s", resulting_url)
    raise

  return _shortener_url(shorturl)
