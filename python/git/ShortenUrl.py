from __future__ import absolute_import, division, print_function, unicode_literals

# This is fairly specific to using a Yourls server:  see http://yourls.org/

import urllib
import urllib2

from util import Util

SHORTEN_PART = 'yourls-api.php'

def _get_index(config, auth):
  if config.use_index_url:
    return urllib2.urlopen(auth.index_url).read().strip()
  else:
    return Util.get_and_increment_index_file(config.index_file)


def shorten(url, config, auth):
  def _shortener_url(part):
    return '%s/%s' % (config.shorten_url, part)

  index = _get_index(config)
  shorturl = config.shorten_prefix + index
  data = urllib.urlencode(dict(signature=auth.yourls,
                               action='shorturl',
                               keyword=shorturl,
                               url=url))
  resulting_url = _shortener_url(SHORTEN_PART)
  urllib2.urlopen(resulting_url, data)
  return _shortener_url(shorturl)
