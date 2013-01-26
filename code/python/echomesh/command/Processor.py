from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import File
from echomesh.util import Log

from gittwit.git import Git

LOGGER = Log.logger(__name__)

class Processor(object):
  def __init__(self, echomesh):
    self._echomesh = echomesh

  def process(self, command):
    command = command.strip()
    self._parts = command and command.split(' ')
    if self._parts:
      self._cmd = self._parts[0]
      if self._cmd.startswith('_'):
        return self._error()
      else:
        return getattr(self, self._cmd, self._error)()

  def clear(self): self._remote()
  def halt(self): self._remote()
  def refresh(self): self._remote()
  def rerun(self): self._remote()
  def restart(self): self._remote()
  def shutdown(self): self._remote()
  def stop(self): self._remote()
  def update(self): self._remote()
  def help(self): self._usage()

  def config(self):
    def error():
      LOGGER.error('Usage: config scope command [... command] \n')

    if len(self._parts) < 3:
      return error()

    try:
      scope = CommandFile.resolve_scope(self.parts[1])
    except Exception as e:
      return error(e.message)

    configs = []
    for yaml in self.parts[2:]:
      try:
        configs.extend(File.yaml_load_stream(yaml))
      except:
        return error("Can't parse yaml argument '%s'" % yaml)

    self._remote(config=Merge.merge_all(*configs))

  def nodes(self):
    for peer in self._echomesh.peers.get_peers().itervalues():
      LOGGER.info(peer)

  def quit(self):
    LOGGER.info('quitting')
    return True

  def _remote(self, **kwds):
    self._echomesh.send(type=self._cmd, **kwds)

  def _usage(self, *errors):
    if errors:
      logger = LOGGER.error
      logger(*errors)
    else:
      logger = LOGGER.info
    cmds = (s for s in dir(self) if not s.startswith('_'))
    logger('Commands are %s', ', '.join(cmds))

  def _error(self):
    self._usage("Didn't understand command %s", self._cmd)

