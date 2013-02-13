from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.base import CommandFile
from echomesh.base import Yaml
from echomesh.base import Merge
from echomesh.remote import Registry, System
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

def execute(echomesh, type=None, **data):
  try:
    if not type:
      raise Exception("No type in data %s" % data)
    function = Registry.get(type)
    if not function:
      raise Exception("Didn't understand data type %s" % type)

    return function(echomesh, **data)

  except Exception as e:
    LOGGER.error(str(e))
