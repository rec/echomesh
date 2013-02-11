from __future__ import absolute_import, division, print_function, unicode_literals

if __name__ == '__main__':
  import os.path
  import sys

  def p(msg='.'):
    """Print progress messages while echomesh loads."""
    print(msg, end='')
    sys.stdout.flush()
  p('Loading echomesh')

  from echomesh.base import Path
  p()

  sys.path.append(os.path.join(Path.CODE_PATH, 'external'))
  p()

  from echomesh.base import Config  # Must be the first import.
  p()

  Config.recalculate(args=sys.argv)
  p()

  if not (Config.get('autostart') or len(sys.argv) < 2 or sys.argv[1] != 'autostart'):
    from echomesh.util import Log
    print()
    Log.logger(__name__).info("Not autostarting because autostart=False")
    exit(0)
  p()

  from echomesh.sound import SetOutput
  p()

  SetOutput.set_output(Config.get('audio', 'output', 'route'))
  print('loaded.')

  from echomesh import Echomesh
  echomesh = Echomesh.Echomesh()
  echomesh.start()
  echomesh.join()

  if Config.get('dump_unused_configs'):
    import yaml
    print(yaml.safe_dump(Config.get_unvisited()))
