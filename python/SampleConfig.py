#!/usr/bin/python

# Copy this file to Config.py, and fill in all your customization/secret values.

includeUrl = False  # True to include URL in tweet.
useShortener = False  # True to turn on URL shortening
shortenUrl = 'http://ax.to'  # Fill in your own shortener here.
shortenPrefix = 'e'
indexFile = '/home/tom/shortenIndex.txt'  # Use any file you like here.

gitUser = 'rec'
gitProject = 'echomesh'

auth = dict(
  twitter=dict(
    consumer_key='fill me',
    consumer_secret='fill me',
    access_token_key='fill me',
    access_token_secret='fill me'),

  yourls='fill me')
