from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import Config
from echomesh.util import Log
from echomesh.base import File

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
    # TODO: badly needs fixing.
    filename = self._parts[1]
    config = File.yaml_load_all(filename)
    if config:
      self._echomesh.send(type='config', data=config)
    else:
      LOGGER.error("Didn't get any data from file %s", filename)

  def commit(self):
    # TODO: fix
    _UPDATE_GIT = (
      ('add', 'config/config.yml'),
      ('commit', '-m', '"Automatic checkin of config file"'),
      #  ('push', 'origin', 'master'),
      )

    LOGGER.info('Committing changes to the configuration')
    if Git.run_git_commands(*_UPDATE_GIT):
      LOGGER.info('Changes committed')
    else:
      LOGGER.info('Changes were NOT committed')

  def nodes(self):
    for peer in self._echomesh.peers.get_peers().itervalues():
      LOGGER.info(peer)

  def quit(self):
    LOGGER.info('quitting')
    return True

  def _remote(self):
    self._echomesh.send(type=self._cmd)

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

