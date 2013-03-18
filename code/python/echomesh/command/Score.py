from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.base import Join

import echomesh.command.Register
import echomesh.remote.Register

LOGGER = Log.logger(__name__)

def _perform(action, echomesh_instance, parts):
  names = echomesh_instance.score_master.perform(action, parts)
  if names:
    LOGGER.info('%s %s.', action, Join.join_words(names))
  else:
    LOGGER.error('%s: no results.', action)

def _local(action):
  def f(echomesh_instance, *parts):
    if echomesh_instance.broadcasting():
      echomesh_instance.send(type=action, parts=parts)
    else:
      _perform(action, echomesh_instance, parts)
  return f

def _remote(action):
  def f(echomesh_instance, **data):
    _perform(action, echomesh_instance, data['parts'])

  return f

def _register():
  for command in _COMMANDS:
    echomesh.command.Register.register(_local(command), command,
                                       help_text=_HELP[command],
                                       see_also=_SEE_ALSO[command])
    echomesh.remote.Register.register(_remote(command), command)

_COMMANDS = ['load', 'pause', 'reset', 'run', 'start', 'unload' ]

_SEE_ALSO = {
  'load': ['unload', 'pause', 'run', 'show elements'],
  'pause': ['run', 'unload'],
  'reset': ['run', 'pause'],
  'run': ['load', 'pause'],
  'start': ['reset', 'run'],
  'unload': ['load', 'pause', 'show elements'],
}

_HELP = {
  'load': """
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
""",

  'reset': """
Usage:

  reset ELEMENT [ELEMENT ...]

Resets the named elements to their start time.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.

Example:
  reset Lights   # Resets an existing element called lights.

""",

  'run': """
Usage:

  run ELEMENT [ELEMENT ...]

Starts running the given ELEMENTs which are already in memory.

Examples:
  run Lights   # Runs an existing element called lights.
  run Lights Sound Action Adventure

""",

  'pause': """
Usage: pause ELEMENT [ELEMENT...] | pause *

Pauses one or more Elements, but keeps them in memory.  The special name
"*" pauses all the running elements at once.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.
""",

  'start': """
Usage: start ITEM [ITEM...] | start *

Starts running the given ITEMs.  If they are scores (i.e. end with .yml) then
load them into memory before running them;  otherwise, these must be the names
existing elements.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.

Examples:

  start foo
  start foo.yml
  start foo.yml as bar

""",

  'unload': """
Usage:

  unload ELEMENT [ELEMENT...]

Unloads the given Elements from memory, pauseping them if they're running.
The special name * unloads all the Elements from memory.

If you are in broadcast mode then this command will be sent to all Echomesh
nodes on the network.
""",
}

_register()
