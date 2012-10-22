from __future__ import absolute_import, division, print_function, unicode_literals

from git import Git
from git import ShortenUrl
from git import Twitter

from util import Log
from util import String

TWITTER_SIZE = 140
INTRO = 'COMMIT: '

URL_FORMAT = 'https://github.com/%s/%s/commit/%s'

LOGGER = Log.logger(__name__)

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
  try:
    url = get_commit_url(commit, config, auth)
  except:
    LOGGER.error("Couldn't get commit URL for '%s', '%s'", commit, description)
    raise

  return String.truncate_suffix(INTRO + description, url, Twitter.TWITTER_SIZE)

def twitter_commit(config, auth):
  try:
    text = get_commit_text(config, auth)
  except:
    LOGGER.error('Getting commit text failed')
    return

  try:
    return Twitter.post_update(text, auth, 'tech', '')
  except:
    LOGGER.error("Couldn't send text '%s' to Twitter")

