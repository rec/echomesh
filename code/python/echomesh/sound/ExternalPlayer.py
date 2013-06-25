from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.network import ClientServer
from echomesh.sound import PlayerSetter
from echomesh.util import Dict
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

_ENVELOPE_ERROR = "ExternalPlayer.%s must either be constant or an envelope."

def _fix(player, name):
  part = getattr(player, name)
  if part.is_constant:
    result = part.evaluate()
  elif part.envelope:
    result = part.envelope.description()
  else:
    raise Exception(_ENVELOPE_ERROR % name)
  setattr(player, name, result)

class ExternalPlayer(MasterRunnable):
  _FIELDS = 'file', 'passthrough', 'level', 'pan', 'loops'

  def __init__(self, element, level=1, pan=0, loops=1, **kwds):
    ClientServer.instance()
    super(ExternalPlayer, self).__init__()
    PlayerSetter.set_player(self, element, level=1, pan=0, loops=1, **kwds)
    _fix(self, 'level')
    _fix(self, 'pan')
    data = Dict.from_attributes(self, ExternalPlayer._FIELDS)
    self._write('construct', **data)

  def _write(self, wtype, **data):
    data['type'] = wtype
    data['hash'] = hash(self)
    if not False:
      ClientServer.instance().write(type='audio', data=data)
    else:
      print('!!!', data)

  def _on_run(self):
    self._write('run')

  def _on_begin(self):
    self._write('begin')

  def _on_pause(self):
    self._write('pause')

  def unload(self):
    self._write('unload')
