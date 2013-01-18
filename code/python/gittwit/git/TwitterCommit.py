from __future__ import absolute_import, division, print_function, unicode_literals

import traceback

from gittwit.git import Git
from gittwit.git import ShortenUrl
from gittwit.twitter import Twitter
from gittwit.util import String

from echomesh.util import Log

TWITTER_SIZE = 140
INTRO = 'COMMIT: '

URL_FORMAT = 'https://github.com/%s/%s/commit/%s'
GIT_LOG = ['log', '-n1', '--abbrev=40']

LOGGER = Log.logger(__name__)

def get_commit_url(commit, config, auth):
  url = ''
  if config['shorten']['include_url']:
    url = URL_FORMAT % (config['git']['user'], config['git']['project'], commit)
    if config['shorten']['enable']:
      url = ShortenUrl.shorten(url, config, auth)
    url = ' ' + url

  return url

def most_recent_commit(**kwds):
  lines, returncode = Git.run_git_command(GIT_LOG, **kwds)
  if not returncode:
    return lines[0].split()[1], lines[-1].strip()

def get_commit_text(config, auth):
  res = most_recent_commit(config=config)
  if res:
    commit, description = res
    try:
      url = get_commit_url(commit, config, auth)
    except:
      LOGGER.error("Couldn't get commit URL for '%s', '%s'", commit, description)
      raise

    return String.truncate_suffix(INTRO + description, url, Twitter.TWITTER_SIZE)

  else:
    LOGGER.error('Failed to git commit')
    return None

def twitter_commit(config, auth):
  try:
    text = get_commit_text(config, auth)
  except:
    LOGGER.critical(traceback.format_exc())
    LOGGER.error('Getting commit text failed')
    return

  if text:
    try:
      return Twitter.post_update(text, auth, 'tech', '')
    except:
      LOGGER.error("Couldn't send text '%s' to Twitter")

