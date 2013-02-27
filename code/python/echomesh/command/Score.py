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

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.

Examples:
  load Lights.yml
  load Lights.yml as l1
  load Lights.yml Lights.yml Lights.yml as l1 l2 l3
"""

def load(echomesh_instance, *parts):
  split = Split.pair_split(parts)
  return echomesh_instance.score_master.load_elements(*split), 'Loaded'


RUN_HELP = """
Usage:

  run ITEM [ITEM ...] [as NAME NAME...]

Starts running the given ITEMs.  If they are scores (i.e. end with .yml) then
load them into memory before running them;  otherwise, these must be the names
existing elements.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.

Examples:
  run Lights   # Runs an existing element called lights.
  run Lights.yml  # Runs a score Lights.yml.
  run Lights.yml as l1

"""

def run(echomesh_instance, *parts):
  split = Split.pair_split(parts)
  return echomesh_instance.score_master.run_elements(split), 'Run'


UNLOAD_HELP = """
Usage:

  unload ELEMENT [ELEMENT...]

Unloads the given Elements from memory, stopping them if they're running.
The special name * unloads all the Elements from memory.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.
"""

def unload(echomesh_instance, *parts):
  return echomesh_instance.score_master.unload_help(parts), 'Unloaded'


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
    LOGGER.info('%s %s.', action, String.join_words(*sorted(names)))
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
        ['unload', 'stop', 'run', 'show elements']),
  run=(_local(run), RUN_HELP, ['load', 'stop']),
  stop=(_local(stop), STOP_HELP, ['run', 'unload']),
  unload=(_local(unload), UNLOAD_HELP, ['load', 'stop', 'show elements']),
)

def _remote(function):
  def f(echomesh_instance, **data):
    _print(function, echomesh_instance, data['parts'])

  return f

RemoteRegister.register_all(
  load=(_remote(load)),
  run=(_remote(run)),
  stop=(_remote(stop)),
  unload=(_remote(unload)),
)
