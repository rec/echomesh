from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Merge
from echomesh.base import Name
from echomesh.base import Path
from echomesh.command import Register
from echomesh.command import Scores
from echomesh.sound import Sound
from echomesh.util import Log
from echomesh.util import Registry
from echomesh.util.math import Units

LOGGER = Log.logger(__name__)

SHOW_REGISTRY = Registry.Registry('show command')

def _info(d, spaces='  '):
  s = '\n'.join('%s%s: %s' % (spaces, k, v) for k, v in sorted(d.iteritems()))
  LOGGER.print('\n%s\n' % s)


ADDRESSES_HELP = """
Shows:
  This machine's current IP address.
  This machine's permanent MAC address.
"""
def addresses(echomesh):
  _info(Name.addresses())


BROADCAST_HELP = """
Shows if this echomesh node is in broadcast made, meaning that its run and stop
commands are sent to all other nodes.

When a node is in broadcast mode, the standard "echomesh:" prompt is replaced
by "echomesh!"

"""
def broadcast(echomesh):
  LOGGER.print('Broadcast is ' + ('ON' if echomesh.broadcasting() else 'off'))



NAMES_HELP = """
"show names" shows you the following information about this echomesh node:

  * The machine name (also called the uname for Linux machines).
  * The echomesh name.  This is by default the machine name but can be changed
    in the echomesh configuration.
  * The echomesh tags for this machine, which are also set in the configuration.
"""

def names(echomesh):
  _info(Name.names())

INFO_HELP = """
"show info" shows your machine's info record.

Info is the list of identifying information sent from your machine to other
echomesh nodes - it is how you see remote nodes identified when you "show nodes"
and it's how your machine will be identified remotely.

info is made up of the "names" and "addresses" of this machine.

See "help show names" and "help show addresses" for more information.

"""

def info(echomesh):
  _info(Name.info())

DIRECTORIES_HELP = """
"show path" shows directories that contain files used by echomesh:

  * The asset directory, where images, audio and other assets are stored.
  * The code directory, where the echomesh Python code is stored.
  * The command directory, which holds configuration files and scores.
  * The project directory, the project root containing assets and commands.
  * The echomesh directory, which is the root of the echomesh installation.
"""
def directories(echomesh):
  _info(Path.info())

NODES_HELP = """
Each echomesh node knows about a list of other nodes on the same network.

"show nodes" lists "info" for each known node on the network, including itself.

See "help show info" for more information.
"""

def nodes(echomesh):
  for name, peer in echomesh.peers.get_peers().iteritems():
    LOGGER.print('%s: ' % name)
    _info(peer)

RUNNING_HELP = """
"show running" shows all the elements now running, as well as the time they were
started.

See "help start" and "help stop" for more information.
"""

def running(echomesh):
  LOGGER.print('Job name  Running Time')
  _info(echomesh.score_master.info())

SOUND_HELP = """
Show all the sound interfaces available on this machine.
"""

def sound(echomesh):
 _info(Sound.info())

UNITS_HELP = """
echomesh understands data expressed in a variety of units like Hz, percent,
semitones and decibels.  "show units" lists these units and their synonyms
(like seconds, sec, s or second).

"""

def units(echomesh):
  LOGGER.print('\nUnits are: %s', Units.list_units())

SHOW_REGISTRY.register_all(
  addresses=(addresses, ADDRESSES_HELP),
  broadcast=(broadcast, BROADCAST_HELP),
  directories=(directories, DIRECTORIES_HELP),
  info=(info, INFO_HELP),
  names=(names, NAMES_HELP),
  nodes=(nodes, NODES_HELP),
  running=(running, RUNNING_HELP),
  scopes=(Scores.scopes, Scores.SCOPES_HELP),
  scores=(Scores.scores, Scores.SCORES_HELP),
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
        function(echomesh)
      else:
        raise Exception("Didn't understand command 'show %s'. %s" %
                        (name, SHOW_USAGE))
SHOW_HELP = """"show" displays information about the current echomesh instance.

""" + SHOW_USAGE

Register.register_all(show=(_show, SHOW_HELP))
