from __future__ import absolute_import, division, print_function, unicode_literals

import echomesh

WINDOW = None

def callback():
  global WINDOW
  WINDOW = echomesh.TinyWindow()
  WINDOW.show()

echomesh.start_application(callback)
