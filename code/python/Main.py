from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config  # Must be the first import in the main file.

from echomesh import Echomesh
from echomesh.sound import SetOutput

def startup():
  if Config.get('autostart') or len(sys.argv) < 2 or sys.argv[1] != 'autostart':
    SetOutput.set_output(Config.get('audio', 'output', 'route'))
    return True

def shutdown():
  if Config.get('dump_unused_configs'):
    import yaml
    print(yaml.safe_dump(Config.get_unvisited()))

if __name__ == '__main__':
  if startup():
    echomesh = Echomesh.Echomesh()
    echomesh.start()
    echomesh.join()
    shutdown()
  else:
    from echomesh.util import Log
    Log.logger(__name__).info("Not autostarting because autostart=False")
