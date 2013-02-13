from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.command import Registry

from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.sound import Sound
from echomesh.util import Log
from echomesh.util.math import Units

LOGGER = Log.logger(__name__)

def help(echomesh):
  LOGGER.info(Registry.usage())

def info(echomesh):
  info = Merge.merge_all(CommandFile.info(), Path.info())
  info = '\n'.join('%s: %s' % i for i in info.iteritems())
  LOGGER.info('\n%s\n', info)

def nodes(echomesh):
  for name, peer in echomesh.peers.get_peers().iteritems():
    info = '\n'.join('  %s: %s' % kv for kv in peer.iteritems())
    LOGGER.info('\n%s:\n%s\n', name, info)

def scores(echomesh):
  LOGGER.info(', '.join(echomesh.score_master.score_names()))

def sound(echomesh):
  Sound.list_ports()

def units(echomesh):
  LOGGER.info('\nUnits are: %s', Units.list_units())

Registry.register_all(
  help=help,
  info=info,
  nodes=nodes,
  scores=scores,
  sound=sound,
  units=units
)
