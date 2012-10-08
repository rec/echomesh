#!/usr/bin/python

import twitter

import Util

TWITTER_SIZE = 140

def getApi(config):
  return twitter.Api(**config.auth['twitter'])

def postUpdate(text, config):
  getApi(config).PostUpdate(Util.truncate(text, TWITTER_SIZE))
