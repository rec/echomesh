from __future__ import absolute_import, division, print_function, unicode_literals

from git import Git
from git import ShortenUrl
from git import Twitter

from util import String

TWITTER_SIZE = 140
INTRO = 'COMMIT: '

URL_FORMAT = 'https://github.com/%s/%s/commit/%s'

def get_commit_url(commit, config, auth):
  url = ''
  if config['shorten']['include_url']:
    url = URL_FORMAT % (config['git']['user'], config['git']['project'], commit)
    if config['shorten']['enable']:
      url = ShortenUrl.shorten(url, config, auth)
    url = ' ' + url

  return url

def get_commit_text(config, auth):
  commit, description = Git.most_recent_commit(config)
  url = get_commit_url(commit, config, auth)
  return String.truncate_suffix(INTRO + description, url, Twitter.TWITTER_SIZE)

def twitter_commit(config, auth):
  text = get_commit_text(config, auth)
  return Twitter.post_update(text, auth, 'tech')
