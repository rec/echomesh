
# This is fairly specific to using a Yourls server:  see http://yourls.org/

import urllib
import urllib2

import Util

SHORTEN_PART = 'yourls-api.php'

def shorten(url, config):
  def shortenerUrl(part):
    return '%s/%s' % (config.shortenUrl, part)

  index = Util.getAndIncrementIndexFile(config.indexFile)
  shorturl = config.shortenPrefix + index
  data = urllib.urlencode(dict(signature=config.auth['yourls'],
                               action='shorturl',
                               keyword=shorturl,
                               url=url))
  urllib2.urlopen(shortenerUrl(SHORTEN_PART), data)
  return shortenerUrl(shorturl)
