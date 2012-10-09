#!/usr/bin/python

# Copy this file to Config.py, and fill in all your customization/secret values.

include_url = False  # True to include URL in tweet.
use_shortener = False  # True to turn on URL shortening
shorten_url = 'http://ax.to'  # Fill in your own shortener here.
shorten_prefix = 'e'
index_file = '/home/tom/shortenIndex.txt'  # Use any file you like here.
index_url = 'http://yoursite.com/sequentialIndex.php'
use_index_url = True

git_binary = '/usr/bin/git'  # Change this if your git is installed in a non-standard place
git_user = 'rec'
git_project = 'echomesh'

discovery_port = 1248

auth = dict(
  twitter=dict(
    consumer_key='fill me',
    consumer_secret='fill me',
    access_token_key='fill me',
    access_token_secret='fill me'),

  yourls='fill me')
