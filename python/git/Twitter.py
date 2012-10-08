#!/usr/bin/python

import twitter

import util.Util

TWITTER_SIZE = 140

def get_api(config):
  return twitter.Api(**config.auth['twitter'])

def post_update(text, config):
  get_api(config).PostUpdate(Util.truncate(text, TWITTER_SIZE))
