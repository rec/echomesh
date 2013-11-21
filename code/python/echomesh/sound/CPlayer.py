from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.sound import PlayerSetter
from echomesh.util import Log
from echomesh.util.thread.Runnable import Runnable

LOGGER = Log.logger(__name__)

class CPlayer(Runnable):
  def __init__(self, element, level=1, pan=0, loops=1, length=-float('inf'),
               **kwds):
    super(CPlayer, self).__init__()
    PlayerSetter.evaluate_player(
      self, element, level=level, pan=pan, loops=loops, length=length, **kwds)
    player = cechomesh.AudioSource(
      self._filename, self._loops, self._begin, self._end,
      self._length, "", 2, self._level, self._pan)
    self._on_run = player.run
    self._on_stop = player.stop
    self._on_stop = player.pause
    self.unload = player.unload
