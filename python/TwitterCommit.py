#!/usr/bin/python

import Config
import Git
import ShortenUrl
import Twitter
import Util

TWITTER_SIZE = 140
INTRO = 'COMMIT: '

URL_PATTERN = 'https://github.com/%s/%s/commit/%s'

def getCommitUrl(commit, config):
  url = ''
  if config.includeUrl:
    url = URL_PATTERN % (config.gitUser, config.gitProject, commit)
    if config.useShortener:
      url = ShortenUrl.shorten(url, config)
    url = ' ' + url

  return url

def getCommitText(config):
  commit, description = Git.mostRecentCommit()
  url = getCommitUrl(commit, config)
  return Util.truncateSuffix(INTRO + description, url, Twitter.TWITTER_SIZE)

def twitterCommit(config):
  Twitter.postUpdate(getCommitText(config), config)

if __name__ == '__main__':
  twitterCommit(Config)

