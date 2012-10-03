#!/usr/bin/python

# This is fairly specific to using a Yourls server:  see http://yourls.org/

import urllib
import urllib2

SHORTEN_PART = 'yourls-api.php'

def _getAndIncrementIndex(f):
  index = '0'
  try:
    index = str(1 + int(open(f).read()))
  except:
    print 'Creating index file', f

  open(f, 'w').write(index)
  return index

def shorten(url, config):
  def shortenerUrl(part):
    return '%/%s' % (config.shortenUrl, part)

  shorturl = config.shortenPrefix + _getAndIncrementIndex(config.indexFile)
  data = urllib.urlencode(dict(signature=config.shortenSignature,
                               action='shorturl',
                               keyword=shorturl,
                               url=url))
  urllib2.urlopen(shortenerUrl(SHORTEN_PART), data)
  return shortenerUrl(shorturl)
