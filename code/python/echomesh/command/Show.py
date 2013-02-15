from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

import echomesh.command.Registry as CommandRegistry
from echomesh.util import Registry

from echomesh.base import Merge
from echomesh.base import Name
from echomesh.base import Path
from echomesh.sound import Sound
from echomesh.util import Log
from echomesh.util.math import Units

LOGGER = Log.logger(__name__)

SHOW_REGISTRY = Registry.Registry('show command')

def _help(echomesh, *parts):
  if not parts:
    LOGGER.print(CommandRegistry.usage())
  else:
    cmd, parts = parts[0], parts[1:]
    if not parts:
      help_text = CommandRegistry.get_help(cmd)
      LOGGER.print(help_text or ('No help text available for "%s"' % cmd))
    elif cmd == 'show':
      sub = parts[0]
      help_text = SHOW_REGISTRY.get_help(sub)
      LOGGER.print(help_text or ('No help text available for "show %s"' % sub))
    else:
      raise Exception("Command '%s' doesn't take any arguments.")

def _info(d):
  s = '\n'.join('  %s: %s' % i for i in sorted(d.iteritems()))
  LOGGER.print('\n\n%s\n' % s)

def names(echomesh):
  _info(Name.info())

def paths(echomesh):
  _info(Path.info())

def nodes(echomesh):
  _info(echomesh.peers.get_peers())

def running(echomesh):
  _info(echomesh.score_master.info())

def sound(echomesh):
  _info(Sound.info())

def units(echomesh):
  LOGGER.print('\nUnits are: %s', Units.list_units())

SHOW_REGISTRY.register_all(
  names=(names, "List all the names and tags belonging to this instance."),
  nodes=nodes,
  paths=paths,
  running=running,
  sound=sound,
  units=units
)

SHOW_NAMES = ' '.join(SHOW_REGISTRY.keys())
SHOW_USAGE = 'You can show the following: %s.' % SHOW_NAMES

def _show(echomesh, *parts):
  name = None
  if parts:
    name, remains = parts[0], parts[1:]
    function = SHOW_REGISTRY.get(name)
    if function:
      function(echomesh, *remains)
    else:
      raise Exception("Didn't understand command 'show %s'. %s" %
                      (name, SHOW_USAGE))
  else:
    LOGGER.print('\n' + SHOW_USAGE)


CommandRegistry.register_all(
  help=_help,
  show=_show,
)
