#!/usr/bin/python

from git import TwitterCommit
from config import Config

if __name__ == '__main__':
  result = TwitterCommit.twitter_commit(Config)
  print 'Twittered', result

