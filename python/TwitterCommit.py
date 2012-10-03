#!/usr/bin/python

import twitter

import ShortenUrl

TWITTER_SIZE = 140
ELLIPSIS = '...'

URL_PATTERN = 'https://github.com/%(user)/%(project)/commit/%(commit)'

def twitterCommit(commit, description, config):
  commitUrl = URL_PATTERN % dict(user=config.gitUser,
                                 project=config.gitProject,
                                 commit=commit)

  shortUrl = ShortenUrl.shorten(commitUrl, config)
  subject = '%s %s' % (shortUrl, description)
  if len(subject) > TWITTER_SIZE:
    subject = subject[0:TWITTER_SIZE - len(ELLIPSIS)] + ELLIPSIS

  twitter.Api(*config.twitterAuth).PostUpdate(subject)
