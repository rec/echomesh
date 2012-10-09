
# This is fairly specific to using a Yourls server:  see http://yourls.org/

import urllib
import urllib2

import util.Util

SHORTEN_PART = 'yourls-api.php'

def _get_index(config):
  if config.use_index_url:
    return urllib2.urlopen(config.index_url).read().strip()
  else:
    return Util.get_and_increment_index_file(config.indexFile)


def shorten(url, config):
  def _shortener_url(part):
    return '%s/%s' % (config.shorten_url, part)

  index = _get_index(config)
  shorturl = config.shorten_prefix + index
  data = urllib.urlencode(dict(signature=config.auth['yourls'],
                               action='shorturl',
                               keyword=shorturl,
                               url=url))
  resultingUrl = _shortener_url(SHORTEN_PART)
  urllib2.urlopen(resultingUrl, data)
  return _shortener_url(shorturl)