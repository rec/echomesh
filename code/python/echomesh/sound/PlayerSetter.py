from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.sound import Util
from echomesh.expression import Expression
from echomesh.util import Log

LOGGER = Log.logger(__name__)

INF = float('inf')

def set_player(player, element,
               level=1, pan=0, loops=1, begin=0, end=INF, length=INF, **kwds):
  player._element = element
  player._file = kwds.pop('file')
  player._filename = Util.DEFAULT_AUDIO_DIRECTORY.expand(player._file)
  if kwds:
    LOGGER.error('Unused keywords %s', kwds)
  player._passthrough = (level == 1 and pan == 0)

  player._length = length
  player._level = Expression.expression(level, element)
  player._pan = Expression.expression(pan, element)
  player._loops = loops
  player._begin = begin
  player._end = end

def _evaluate_player(player, name):
  part = getattr(player, name)
  is_constant = part.is_constant()
  result = {'is_constant': is_constant}
  if is_constant:
    result['value'] = part.evaluate()
  elif part.envelope:
    result['envelope'] = part.envelope.description()
  else:
    raise Exception(_ENVELOPE_ERROR % name)
  setattr(player, name, result)

def evaluated_player(player, element, **kwds):
  set_player(player, element, **kwds)
  _evaluate_player(player, '_level')
  _evaluate_player(player, '_pan')
