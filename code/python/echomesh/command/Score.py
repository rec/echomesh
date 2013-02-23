from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.util import Log
from echomesh.util import Join

LOGGER = Log.logger(__name__)

def _as_parts(parts):
  if 'as' in parts:
    loc = parts.index('as')
    return parts[0:loc], parts[loc + 1:]
  else:
    return parts, None

LOAD_HELP = """
Usage:

  load SCORE [SCORE...] [as NAME NAME...]

Loads the given Scores into memory as Elements but does not start them.

You can specify Element names for the Scores by using the load ... as ...
form - you'll get an error if these names don't exist.

If you don't specify names, each new Element will automatically be given a
unique name based on its Score name.

Examples:

  load Lights
  load Lights.yml
  load Lights.yml as l1
  load Lights Lights Lights as l1 l2 l3
"""


def _print(names, action):
  if names:
    LOGGER.print('%s %s.', action, Join.join_words(*names))
  else:
    LOGGER.error('%s: no results.' % action)


def load(echomesh, *parts):
  _print(echomesh.score_master.load_scores(*_as_parts(parts)), 'Loaded')


RUN_HELP = """
Usage:

  run SCORE [SCORE...] [as NAME NAME...]

Loads the given Scores into memory as Elements and then starts them.
Exactly the same as executing "load" and then "start".
"""

def run(echomesh, *parts):
  _print(echomesh.score_master.run_scores(*_as_parts(parts)), 'Run')


UNLOAD_HELP = """
Usage:

  unload ELEMENT [ELEMENT...]

Unloads the given Elements from memory, stopping them if they're running.
The special name * unloads all the Elements from memory.
"""

def unload(echomesh, *parts):
  _print(echomesh.score_master.unload_elements(parts), 'Unloaded')


START_HELP = """
Usage: start element [element...] | start *

Starts one or more Elements running.  The special name * will start all the
loaded Elements at once.
"""

def start(echomesh, *parts):
  _print(echomesh.score_master.start_elements(parts), 'Started')

STOP_HELP = """
Usage: stop element [element...] | stop *

Stops one or more Elements, but keeps them in memory.  The special name
"*" stops all the running elements at once.
"""

def stop(echomesh, *parts):
  _print(echomesh.score_master.stop_elements(parts), 'Stopped')

Register.register_all(
  load=(load, LOAD_HELP, ['unload', 'start', 'stop', 'run', 'show elements']),
  run=(run, RUN_HELP, ['load', 'start', 'stop']),
  start=(start, START_HELP, ['run', 'stop']),
  stop=(stop, STOP_HELP, ['start', 'unload']),
  unload=(unload, UNLOAD_HELP, ['load', 'stop', 'show elements']),
)
