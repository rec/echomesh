from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Registry
from echomesh.util import Log
from echomesh.util import Join

LOGGER = Log.logger(__name__)

def _stop_or_start(message, doer, scores):
  try:
    if not scores:
      raise Exception('Usage: %s scorefile' % message)

    results = []
    for score in scores:
      results.extend(doer(score))

    past = 'Stopped' if message == 'stop' else 'Started'
    for name in results:
      LOGGER.info('%s %s.', past, name)

  except Exception as e:
    LOGGER.print_error("Couldn't %s %s", message, Join.join_words(*scores),
                       exc_info=1)


def start(echomesh, *scores):
  _stop_or_start('start', echomesh.score_master.start_score, scores)


START_HELP = """
Usage: start score [score...]

Starts one or more scores running.  The command "show running" show all the
scores that are currently running.
"""

def stop(echomesh, *scores):
  _stop_or_start('stop', echomesh.score_master.stop_score, scores)

STOP_HELP = """
Usage: stop score [score...] | *

Stops one or more scores.  The special score name '*' stops all the running
scores at once.
"""

Registry.register_all(
  start=(start, START_HELP),
  stop=(stop, STOP_HELP),
)

