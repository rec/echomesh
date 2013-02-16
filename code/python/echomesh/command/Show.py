from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import time

import echomesh.command.Registry as CommandRegistry

from echomesh.base import Merge
from echomesh.base import Name
from echomesh.base import Path
from echomesh.sound import Sound
from echomesh.util import Flag
from echomesh.util import Log
from echomesh.util import Registry
from echomesh.util import Scope
from echomesh.util import SizeName
from echomesh.util.math import Units

LOGGER = Log.logger(__name__)

SHOW_REGISTRY = Registry.Registry('show command')

def _info(d, spaces='  '):
  s = '\n'.join('%s%s: %s' % (spaces, k, v) for k, v in sorted(d.iteritems()))
  LOGGER.print(s)

ADDRESSES_HELP = """
Shows:
  This machine's current IP address.
  This machine's permanent MAC address.
"""
def addresses(echomesh):
  _info(Name.addresses())

BROADCAST_HELP = """
Shows if this echomesh is in broadcast made, meaning that run and stop commands
are sent to all other nodes.
"""
def broadcast(echomesh):
  LOGGER.print('Broadcast is ' + ('ON' if echomesh.broadcasting() else 'off'))


def _time(t):
  return time.strftime('%H:%M', time.localtime(t))

ELEMENT_FORMAT = '%-28s %5s %9s %9s %9s'

def _elements(path, resolve=False, scope='all', recursive=False):
  printed = False
  if scope == 'all':
    for s in Scope.SCOPES:
      printed = _elements(path, resolve, s, recursive) or printed
  else:
    scope = Scope.resolve(scope)
    pathdir = os.path.join(Path.COMMAND_PATH, scope, 'element', path)
    if os.path.isdir(pathdir):
      printed_this_time = False
      for f in sorted(os.listdir(pathdir)):
        joined_f = os.path.join(pathdir, f)
        is_dir = os.path.isdir(joined_f)
        if not (is_dir or f.endswith('yml')):
          continue
        if not printed_this_time:
          printed_this_time = True
          if not printed:
            LOGGER.print(ELEMENT_FORMAT, 'File name', 'Size', 'Accessed',
                         'Modified', 'Created')
            printed = True
          else:
            LOGGER.print('\n')
          LOGGER.print('  %s/%s:', scope, path)
        if is_dir:
          LOGGER.print('    %s/', f)
        else:
          stat = os.stat(joined_f)
          LOGGER.print(ELEMENT_FORMAT,
                       '    ' + f, SizeName.size_name(stat.st_size),
                       _time(stat.st_atime),
                       _time(stat.st_mtime),
                       _time(stat.st_ctime))
  return printed


ELEMENTS_HELP = """
Shows all the elements in all contexts
"""
def elements(echomesh, *args):
  flags, paths = Flag.split_args(args)
  paths = paths or ['']
  for p in paths:
    _elements(p, **flags)


NAMES_HELP = """
Shows:
  The machine name (also called the uname).
  The echomesh name.
  Any echomesh tags for this machine.
"""

def names(echomesh):
  _info(Name.names())

INFO_HELP = """
Shows the machine's "info", the list of identifying information sent from your
machine to other echomesh nodes, which is a combination of the information from
"show names" and "show addresses".
"""

def info(echomesh):
  _info(Name.info())

PATHS_HELP = """
Paths are directories referenced by echomesh.

Shows:
  The asset path, where images, audio and other assets are stored.
  The code path, where the echomesh Python code is stored.
  The command path, which holds configuration files and scores for your project.
  The project path, the root of your project which holds assets and commands.
  The echomesh path, which is the root of the echomesh installation.
"""
def paths(echomesh):
  _info(Path.info())

NODES_HELP = """
Shows a list of other echomesh nodes that have been detected on this network,
together with their info.
"""

def nodes(echomesh):
  for name, peer in echomesh.peers.get_peers().iteritems():
    LOGGER.print('%s: ' % name)
    _info(peer)

RUNNING_HELP = """
Shows all the scores that are now running, as well as the time they were
started.
"""

def running(echomesh):
  _info(echomesh.score_master.info())

SOUND_HELP = """
Show all the sound interfaces available on this machine.
"""

def sound(echomesh):
  _info(Sound.info())

UNITS_HELP = """
Show the possible units that can be used in echomesh scores.
"""

def units(echomesh):
  LOGGER.print('\nUnits are: %s', Units.list_units())

SHOW_REGISTRY.register_all(
  addresses=(addresses, ADDRESSES_HELP),
  broadcast=(broadcast, BROADCAST_HELP),
  elements=(elements, ELEMENTS_HELP),
  info=(info, INFO_HELP),
  names=(names, NAMES_HELP),
  nodes=(nodes, NODES_HELP),
  paths=(paths, PATHS_HELP),
  running=(running, RUNNING_HELP),
  sound=(sound, SOUND_HELP),
  units=(units, UNITS_HELP),
)

SHOW_NAMES = SHOW_REGISTRY.join_keys()
SHOW_USAGE = 'You can show any of the following values: %s.\n' % SHOW_NAMES

def _show(echomesh, *parts):
  if not parts:
    LOGGER.print('\n' + SHOW_USAGE)
  else:
    for name in parts:
      function = SHOW_REGISTRY.get(name)
      if function:
        LOGGER.print()
        function(echomesh)
        LOGGER.print()
      else:
        raise Exception("Didn't understand command 'show %s'. %s" %
                        (name, SHOW_USAGE))
SHOW_HELP = """"show" displays information about the current echomesh instance.

""" + SHOW_USAGE

def _help(echomesh, *parts):
  LOGGER.print()
  if not parts:
    LOGGER.print('echomesh has the following commands: ' +
                 CommandRegistry.join_keys())
  else:
    cmd, parts = parts[0], parts[1:]
    if not parts:
      help_text = CommandRegistry.get_help(cmd)
      LOGGER.print(help_text or ('No help text available for "%s"' % cmd))
    elif cmd == 'show':
      sub = parts[0]
      help_text = SHOW_REGISTRY.get_help(sub)
      LOGGER.print('show %s:' % sub)
      LOGGER.print(help_text or ('No help text available for "show %s"' % sub))
    else:
      raise Exception("Command '%s' doesn't take any arguments.")


HELP_HELP = """
"help" lets you get information about echomesh commands.

You can get help on the following commands:

  """ + CommandRegistry.join_keys()

CommandRegistry.register_all(show=(_show, SHOW_HELP),
                             help=(_help, HELP_HELP))

