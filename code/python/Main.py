from __future__ import absolute_import, division, print_function, unicode_literals


import sys

def _p(msg='.'):
  print(msg, end='')
  sys.stdout.flush()

_p('Loading echomesh')

_p()

from echomesh.base import Config  # Must be the first import in the main file.

_p()

Config.recalculate(args=sys.argv)

_p()

from echomesh import Echomesh
from echomesh.sound import SetOutput

_p()

def startup():
  if Config.get('autostart') or len(sys.argv) < 2 or sys.argv[1] != 'autostart':
    SetOutput.set_output(Config.get('audio', 'output', 'route'))
    return True

def shutdown():
  if Config.get('dump_unused_configs'):
    import yaml
    print(yaml.safe_dump(Config.get_unvisited()))

if __name__ == '__main__':
  _p()
  if startup():
    _p()
    echomesh = Echomesh.Echomesh()
    print('Loaded.')
    echomesh.start()
    echomesh.join()
    shutdown()
  else:
    from echomesh.util import Log
    Log.logger(__name__).info("Not autostarting because autostart=False")
