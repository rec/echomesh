from __future__ import absolute_import, division, print_function, unicode_literals

from git import TwitterCommit

from config import Auth
from config import Config

if __name__ == '__main__':
  result = TwitterCommit.twitter_commit(Config.config(), Auth.AUTH)
  print('Twittered', result)

