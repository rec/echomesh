from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.expression.Envelope import Envelope
from echomesh.sound import PlayerSetter
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class CPlayer(MasterRunnable):
  def __init__(self, element, level=1, pan=0, loops=1, length=-1, **kwds):
    super(CPlayer, self).__init__()
    PlayerSetter.evaluate_player(
      self, element, level=level, pan=pan, loops=loops, length=length, **kwds)
    self.player = cechomesh.AudioSource(
      self._filename, self._loops, self._begin, self._end,
      self._length, "", 2, self._level, self._pan, self.pause)

  def __del__(self):
    super(CPlayer, self).__del__()
    self.unload()

  def _on_begin(self):
    return self.player.begin()

  def _on_run(self):
    return self.player.run()

  def _on_pause(self):
    return self.player.pause()

  def unload(self):
    super(CPlayer, self).unload()
    LOGGER.debug('unload')
    self.player.unload()
