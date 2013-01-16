#!/usr/local/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.network import SearchTwitter
from echomesh.util.thread import Closer

if __name__ == '__main__':
  with Closer.Closer() as closer:
    tags = []
    while closer.is_open:
      tag = raw_input('Enter a tag or quit to exit\n').strip()
      if tag == 'quit':
        closer.close()
      else:
        tags.append(tag)
        print('Now following', *tags)
        loop = SearchTwitter.Loop(tag, print)
        loop.start()
        closer.add_openable(loop)

