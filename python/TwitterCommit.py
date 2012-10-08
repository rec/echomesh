#!/usr/bin/python

import Config
import Git
import ShortenUrl
import Twitter
import Util

TWITTER_SIZE = 140
INTRO = 'COMMIT: '

URL_PATTERN = 'https://github.com/%s/%s/commit/%s'

def get_commit_url(commit, config):
  url = ''
  if config.include_url:
    url = URL_PATTERN % (config.git_user, config.git_project, commit)
    if config.use_shortener:
      url = ShortenUrl.shorten(url, config)
    url = ' ' + url

  return url

def get_commit_text(config):
  commit, description = Git.most_recent_commit(config)
  url = get_commit_url(commit, config)
  return Util.truncate_suffix(INTRO + description, url, Twitter.TWITTER_SIZE)

def twitter_commit(config):
  text = get_commit_text(config)
  Twitter.post_update(text, config)
  return text

if __name__ == '__main__':
  print 'Twittered', twitter_commit(Config)

