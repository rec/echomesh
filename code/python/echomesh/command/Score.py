from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Registry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def start(echomesh, *parts):
  if len(parts) < 2:
    return LOGGER.error('Usage: start scorefile')
  scorefile = parts[1]
  if echomesh.score_master.start_score(scorefile):
    LOGGER.info('Started score %s', scorefile)
  else:
    LOGGER.error('Failed to start score %s', scorefile)

def stop(echomesh, *parts):
  if len(parts) < 2:
    return LOGGER.error('Usage: stop scorefile')
  scorefile = parts[1]
  score = echomesh.score_master.get_score(scorefile)
  if score:
    score.stop()
    LOGGER.info("Stopped score %s", scorefile)
  else:
    LOGGER.error("Couldn't find score %s", scorefile)

Registry.register_all(
  start=start,
  stop=stop,
)

