from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Registry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def start(echomesh, *parts):
  if len(parts) < 2:
    return LOGGER.print_error('Usage: start scorefile')
  scorefile = parts[1]
  if echomesh.score_master.start_score(scorefile):
    LOGGER.print('Started score %s', scorefile)
  else:
    LOGGER.print_error('Failed to start score %s', scorefile)

START_HELP = """
Usage: start score [score...]

Starts one or more scores running.  The command "show running" will
list all the scores that are current running and their names.
"""

def stop(echomesh, *parts):
  if len(parts) < 2:
    return LOGGER.print_error('Usage: stop scorefile')
  scorefile = parts[1]
  score = echomesh.score_master.get_score(scorefile)
  if score:
    score.stop()
    LOGGER.print("Stopped score %s", scorefile)
  else:
    LOGGER.print_error("Couldn't find score %s", scorefile)

STOP_HELP = """
Usage: stop score [score...] | *

Stops one or more scores.  The special score name '*' stops all the running
scores at once.
"""

Registry.register_all(
  start=(start, START_HELP),
  stop=(stop, STOP_HELP),
)

