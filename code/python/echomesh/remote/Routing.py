from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import CommandFile
from echomesh.base import Yaml
from echomesh.base import Merge
from echomesh.remote import RemoteRegistry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def peer(instance, **data):
  instance.peers.new_peer(data)

def event(instance, **data):
  instance.handle(data)

def config(_, scope, cfg):
  f = CommandFile.config_file(scope)
  configs = Yaml.read(f) + [cfg]
  Yaml.write(f, Merge.merge(*configs))
  # TODO: needs to propagate!
  LOGGER.info('Changing configuration for %s', scope)

RemoteRegistry.register_all(
  config=config,
  event=event,
  peer=peer,
)
