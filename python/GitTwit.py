from __future__ import absolute_import, division, print_function, unicode_literals

from git import TwitterCommit

from config import Auth
from config import Config
from util import Log

if __name__ == '__main__':
  result = TwitterCommit.twitter_commit(Config.CONFIG, Auth.AUTH)
  if result:
    Log.logger(__name__).info('Twittered %s', result)

