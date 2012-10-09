from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config

from git import Git
from git import ShortenUrl
from git import Twitter

from util import Util

TWITTER_SIZE = 140
INTRO = 'COMMIT: '

URL_PATTERN = 'https://github.com/%s/%s/commit/%s'

def get_commit_url(commit, config, auth):
  url = ''
  if config.include_url:
    url = URL_PATTERN % (config.git_user, config.git_project, commit)
    if config.use_shortener:
      url = ShortenUrl.shorten(url, config, auth)
    url = ' ' + url

  return url

def get_commit_text(config, auth):
  commit, description = Git.most_recent_commit(config)
  url = get_commit_url(commit, config, auth)
  return Util.truncate_suffix(INTRO + description, url, Twitter.TWITTER_SIZE)

def twitter_commit(config, auth):
  text = get_commit_text(config, auth)
  Twitter.post_update(text, auth)
  return text
