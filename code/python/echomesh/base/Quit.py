from __future__ import absolute_import, division, print_function, unicode_literals

import atexit

QUITTING = False
HANDLERS = []
PRINT_EXCEPTIONS = not False

def register_atexit(handler):
  HANDLERS.append(handler)

def request_quit():
  print('request_quit')
  global QUITTING
  QUITTING = True
  for h in HANDLERS:
    try:
      h()
    except Exception as e:
      if PRINT_EXCEPTIONS:
        print('Exception during quit:', e)

def _atexit_quit():
  if QUITTING:
    reason = 'at your request'
  else:
    reason = 'due to a fatal error'
    request_quit()

  print('echomesh shut down %s.' % reason)

atexit.register(_atexit_quit)
