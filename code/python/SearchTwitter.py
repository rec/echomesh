#!/usr/local/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.network import SearchTwitter
from echomesh.util.thread import Closer

def print_twitter(twitter):
  print('name:', twitter['user_name'])
  print('text:', twitter['text'])
  print()

CLOSER = Closer.Closer()

TAGS = []

def add_hashtag(*tags):
  for tag in tags:
    if not tag.startswith('#'):
      tag = '#' + tag
    TAGS.append(tag)
    loop = SearchTwitter.Loop(tag, print_twitter)
    loop.start()
    CLOSER.add_openable(loop)
  print('Now following', *TAGS)

if __name__ == '__main__':
  import sys

  add_hashtag(*sys.argv[1:])
  while CLOSER.is_open:
    tag = raw_input('Enter a tag or quit to exit\n').strip()
    if tag == 'quit':
      CLOSER.close()
    elif tag:
      add_hashtag(tag)

