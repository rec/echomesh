#!/usr/bin/python

import twitter

import Config
import Git
import ShortenUrl

TWITTER_SIZE = 140
ELLIPSIS = '...'

URL_PATTERN = 'https://github.com/%s/%s/commit/%s'

def postUpdate(update, config):
  if len(update) > TWITTER_SIZE:
    update = update[0:TWITTER_SIZE - len(ELLIPSIS)] + ELLIPSIS

  # TODO: why didn't this work?
  #  twitter.Api(*config.auth['twitter']).PostUpdate(update)
  auth = config.auth['twitter']
  twitter.Api(
    consumer_key = auth['consumer_key'],
    consumer_secret = auth['consumer_secret'],
    access_token_key = auth['access_token_key'],
    access_token_secret = auth['access_token_secret']
  ).PostUpdate(update)


def addUrlToSubject(commit, subject, config):
  url = URL_PATTERN % (config.gitUser, config.gitProject, commit)
  if config.useShortener:
    url = ShortenUrl.shorten(url, config)

  return '%s %s' % (url, subject)

def twitterCommit(config):
  commit, subject = Git.mostRecentCommit()
  if config.includeUrl:
    subject = addUrlToSubject(commit, subject, config)

  postUpdate(subject, config)

if __name__ == '__main__':
  twitterCommit(Config)

