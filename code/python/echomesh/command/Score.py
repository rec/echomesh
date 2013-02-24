from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register as CommandRegister
from echomesh.util import Log
from echomesh.util import Split
from echomesh.util import String
from echomesh.remote import Register as RemoteRegister


LOGGER = Log.logger(__name__)

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

def load(echomesh_instance, *parts):
  split = Split.split_list(parts, 'as')
  return echomesh_instance.score_master.load_scores(*split), 'Loaded'


RUN_HELP = """
Usage:

  run SCORE [SCORE...] [as NAME NAME...]

Loads the given Scores into memory as Elements and then starts them.
Exactly the same as executing "load" and then "start".

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.
"""

def run(echomesh_instance, *parts):
  split = Split.split_list(parts, 'as')
  return echomesh_instance.score_master.run_scores(*split), 'Run'


UNLOAD_HELP = """
Usage:

  unload ELEMENT [ELEMENT...]

Unloads the given Elements from memory, stopping them if they're running.
The special name * unloads all the Elements from memory.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.
"""

def unload(echomesh_instance, *parts):
  return echomesh_instance.score_master.unload_elements(parts), 'Unloaded'


START_HELP = """
Usage: start element [element...] | start *

Starts one or more Elements running.  The special name * will start all the
loaded Elements at once.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.
"""

def start(echomesh_instance, *parts):
  return echomesh_instance.score_master.start_elements(parts), 'Started'

STOP_HELP = """
Usage: stop element [element...] | stop *

Stops one or more Elements, but keeps them in memory.  The special name
"*" stops all the running elements at once.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.
"""

def stop(echomesh_instance, *parts):
  return echomesh_instance.score_master.stop_elements(parts), 'Stopped'

def _print(function, echomesh_instance, parts):
  names, action = function(echomesh_instance, *parts)
  if names:
    LOGGER.print('%s %s.', action, String.join_words(*names))
  else:
    LOGGER.error('%s: no results.' % action)

def _local(function):
  def f(echomesh_instance, *parts):
    if echomesh_instance.broadcasting():
      echomesh_instance.send(type=function.__name__, parts=parts)
    else:
      _print(function, echomesh_instance, parts)
  return f

CommandRegister.register_all(
  load=(_local(load), LOAD_HELP,
        ['unload', 'start', 'stop', 'run', 'show elements']),
  run=(_local(run), RUN_HELP, ['load', 'start', 'stop']),
  start=(_local(start), START_HELP, ['run', 'stop']),
  stop=(_local(stop), STOP_HELP, ['start', 'unload']),
  unload=(_local(unload), UNLOAD_HELP, ['load', 'stop', 'show elements']),
)

def _remote(function):
  def f(echomesh_instance, **data):
    _print(function, echomesh_instance, data['parts'])

  return f

RemoteRegister.register_all(
  load=(_remote(load)),
  run=(_remote(run)),
  start=(_remote(start)),
  stop=(_remote(stop)),
  unload=(_remote(unload)),
)
