#!/usr/local/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.network import SearchTwitter

if __name__ == '__main__':
  import sys

  try:
    query = sys.argv[1]
  except:
    query = '#aaronswartz'

  loop = SearchTwitter.Loop(query, print)
  loop.start()
  raw_input('Press return to exit\n')
  loop.close()
  loop.join()

