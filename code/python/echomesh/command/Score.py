from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.util import Log
from echomesh.util import Join

LOGGER = Log.logger(__name__)


LOAD_HELP = """
Usage: load SCORE [SCORE...] [as NAME NAME...]

Examples:

load foo
load foo.yml

"""

def _stop_or_start(message, doer, elements):
  try:
    if not elements:
      raise Exception('Usage: %s element [element...]' % message)

    results = []
    for score in elements:
      results.extend(doer(score))

    past = 'Stopped' if message == 'stop' else 'Started'
    for name in results:
      LOGGER.info('%s %s.', past, name)

  except Exception as e:
    LOGGER.print_error("Couldn't %s %s", message, Join.join_words(*elements),
                       exc_info=1)


def start(echomesh, *elements):
  _stop_or_start('start', echomesh.score_master.start_score, elements)


START_HELP = """
Usage: start element [element...]

Starts one or more elements running.  The command "show elements" will show all the
elements that are currently running.
"""

def stop(echomesh, *elements):
  _stop_or_start('stop', echomesh.score_master.stop_score, elements)

STOP_HELP = """
Usage: stop element [element...] | *

Stops one or more elements.  The special element name '*' stops all the running
elements at once.
"""

Register.register_all(
  load=(load, LOAD_HELP),
  run=(run, RUN_HELP),
  start=(start, START_HELP),
  stop=(stop, STOP_HELP),
  unload=(unload, UNLOAD_HELP),
)
