from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.util import Log
from echomesh.util import Join

LOGGER = Log.logger(__name__)

######## TODO

LOAD_HELP = """
Usage:

  load SCORE [SCORE...] [as NAME NAME...]

Loads the given scores into memory as elements but does not start them.

You can specify element names for the scores by using the load ... as ...
form - you'll get an error if these names don't exist.

If you don't specify names, each new element will automatically be given a
unique name based on its score name.

Examples:

  load Lights
  load Lights.yml
  load Lights.yml as l1
  load Lights Lights Lights as l1 l2 l3

See also "help unload", "help start", "help stop", "help run".
"""



def load(echomesh):
  pass

RUN_HELP = """
Usage:

  run SCORE [SCORE...] [as NAME NAME...]

Loads the given scores and then starts them.

See also "help load", "help start",

"""

def run(echomesh): pass

UNLOAD_HELP = """
"""

def unload(echomesh): pass

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
