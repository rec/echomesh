from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Settings
from echomesh.base import Join
from echomesh.command import Registry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

GET_ARGUMENT_ERROR = """
"get" needs one or more arguments.

Example:
  get audio.input.enable
"""

def _route_items(items, successes, failures):
  for v in items:
    try:
      successes.append([v, Settings.get(*v.split('.'))])
    except:
      failures.append(v)

def get_settings(_, *items):
  failures = []
  if items:
    successes = []
    for i in items:
      parts = i.split('.')
      try:
        value = Settings.get(*parts)
      except:
        failures.append(i)
      else:
        successes.append([i, value])
  else:
    assignments = Settings.assignments().items()
    successes = [('.'.join(s), v) for s, v in assignments]

  if successes or failures:
    for value, result in successes:
      LOGGER.info('%s=%s', value, result)
    if failures:
      LOGGER.error('Didn\'t understand %s', Join.join_words(failures))
    LOGGER.info('')
  else:
    LOGGER.info('No settings variables have been set.\n')

GET_HELP = """
  Prints one or more settings variables.

Examples:
  settings.get speed
  settings.get audio.input.enabled audio.output.enabled
"""

Registry.registry().register(get_settings, 'get', GET_HELP)
