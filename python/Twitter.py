#!/usr/bin/python

import twitter

import Util

TWITTER_SIZE = 140

def getApi(config):
  return twitter.Api(**config.auth['twitter'])

def postUpdate(text, config):
  getApi(config).PostUpdate(Util.truncate(text, TWITTER_SIZE))

  # twitter.Api(
  #   consumer_key = auth['consumer_key'],
  #   consumer_secret = auth['consumer_secret'],
  #   access_token_key = auth['access_token_key'],
  #   access_token_secret = auth['access_token_secret']
  # ).PostUpdate(update)

  # TODO: why didn't this work?
  #   twitter.Api(*auth).PostUpdate(update)
