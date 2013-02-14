from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.base import CommandFile
from echomesh.base import Yaml
from echomesh.base import Merge
from echomesh.remote import Registry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def peer(echomesh, **data):
  echomesh.peers.new_peer(data)

def event(echomesh, **data):
  echomesh.receive_event(data)

def config(echomesh, scope, config):
  f = CommandFile.config_file(scope)
  configs = Yaml.read(f) + [config]
  Yaml.write(f, Merge.merge(*configs))
  # TODO: needs to propagate!
  LOGGER.info('Changing configuration for %s', scope)

Registry.register_all(
  config=config,
  event=event,
  peer=peer,
)
