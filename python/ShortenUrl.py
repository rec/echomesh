
# This is fairly specific to using a Yourls server:  see http://yourls.org/

import urllib
import urllib2

import Util

SHORTEN_PART = 'yourls-api.php'

def getIndex(config):
  if config.useIndexUrl:
    return urllib2.urlopen(config.indexUrl).read().strip()
  else:
    return Util.getAndIncrementIndexFile(config.indexFile)


def shorten(url, config):
  def shortenerUrl(part):
    return '%s/%s' % (config.shortenUrl, part)

  index = getIndex(config)
  shorturl = config.shortenPrefix + index
  data = urllib.urlencode(dict(signature=config.auth['yourls'],
                               action='shorturl',
                               keyword=shorturl,
                               url=url))
  resultingUrl = shortenerUrl(SHORTEN_PART)
  urllib2.urlopen(resultingUrl, data)
  return shortenerUrl(shorturl)
