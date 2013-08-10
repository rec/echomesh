from __future__ import absolute_import, division, print_function, unicode_literals

import atexit

QUITTING = False
HANDLERS = []
PRINT_EXCEPTIONS = not False
_REGISTERED = False

def register_atexit(handler):
  HANDLERS.append(handler)
  if not _REGISTERED:
    _register_quit()

def request_quit():
  global QUITTING
  QUITTING = True
  for h in HANDLERS:
    try:
      h()
    except Exception as e:
      if PRINT_EXCEPTIONS:
        print('Exception during quit:', e)

def _register_quit():
  global _REGISTERED
  _REGISTERED = True
  def atexit_quit():
    if QUITTING:
      reason = 'at your request'
    else:
      reason = 'due to a fatal error'
      request_quit()

    print('echomesh shut down %s.' % reason)
  atexit.register(atexit_quit)
