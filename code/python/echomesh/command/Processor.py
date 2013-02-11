from __future__ import absolute_import, division, print_function, unicode_literals

import time
import traceback

from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.base import Yaml
from echomesh.sound import Sound
from echomesh.util import Log
from echomesh.util import Scope
from echomesh.util.math import Units

from gittwit.git import Git

LOGGER = Log.logger(__name__)

class Processor(object):
  def __init__(self, echomesh):
    self._echomesh = echomesh

  def __call__(self, command):
    try:
      command = command.strip()
      self._parts = command and command.split(' ')
      if self._parts:
        self._cmd = self._parts[0]
        if self._cmd.startswith('_'):
          return self._error()
        else:
          return getattr(self, self._cmd, self._error)()
    except Exception as e:
      LOGGER.error('%s', str(e))
      LOGGER.error(traceback.format_exc())

  def clear(self): self._remote()
  def halt(self): self._remote()
  def refresh(self): self._remote()
  def rerun(self): self._remote()
  def restart(self): self._remote()
  def shutdown(self): self._remote()
  def stop(self): self._remote()
  def update(self): self._remote()
  def help(self): self._usage()
  def sound(self): Sound.list_ports()
  def units(self):
    LOGGER.info('\nUnits are: %s', Units.list_units())

  def scores(self):
    LOGGER.info(', '.join(self._echomesh.score_master.score_names()))

  def info(self):
    info = Merge.merge_all(CommandFile.info(), Path.info())
    info = '\n'.join('%s: %s' % i for i in info.iteritems())
    LOGGER.info('\n%s\n', info)

  def start(self):
    if len(self._parts) < 2:
      return LOGGER.error('Usage: start scorefile')
    scorefile = self._parts[1]
    if self._echomesh.score_master.start_score(scorefile):
      LOGGER.info('Started score %s', scorefile)
    else:
      LOGGER.error('Failed to start score %s', scorefile)

  def stop(self):
    if len(self._parts) < 2:
      return LOGGER.error('Usage: stop scorefile')
    scorefile = self._parts[1]
    score = self._echomesh.score_master.get_score(scorefile)
    if score:
      score.stop()
      LOGGER.info("Stopped score %s", scorefile)
    else:
      LOGGER.error("Couldn't find score %s", scorefile)

  def config(self):
    if len(self._parts) < 2:
      return LOGGER.error('Usage: config scope command [... command] ')

    try:
      scope = Scope.resolve(self._parts[1])
    except Exception as e:
      return LOGGER.error(e.message)

    if len(self._parts) == 2:
      try:
        config = open(CommandFile.config_file(scope), 'r').read()
        LOGGER.info('\n' + config)
      except IOError:
        LOGGER.info('(none)')
      return

    try:
      parts = ' '.join(self._parts[2:])
      configs = Yaml.decode(parts)
    except:
      return LOGGER.error("Can't parse yaml argument '%s'" % yaml)

    config = Merge.merge_all_strict(*configs)
    if '0.local' in scope:
      self._echomesh.socket.router({'type': 'config', 'config': config,
                                    'scope': scope})
    elif '4.default' in scope:
      LOGGER.error("Can't make changes to default scope")
    else:
      self._remote(scope=scope, config=config)

  def nodes(self):
    for name, peer in self._echomesh.peers.get_peers().iteritems():
      info = '\n'.join('  %s: %s' % kv for kv in peer.iteritems())
      LOGGER.info('\n%s:\n%s\n', name, info)

  def quit(self):
    LOGGER.debug('quitting')
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
    logger('\nCommands are:\n  %s', ', '.join(cmds))

  def _error(self):
    self._usage("\nDidn't understand command %s", self._cmd)

