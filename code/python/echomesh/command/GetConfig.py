from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.command import CommandRegistry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

GET_ARGUMENT_ERROR = """
"get" needs one or more arguments.

Example:
  get audio.input.enable
"""

def get_config(_, *items):
  if not items:
    raise Exception(GET_ARGUMENT_ERROR)
  errors = []
  successes = []
  for v in items:
    try:
      successes.append([v, Config.get(*v.split('.'))])
    except:
      errors.append(v)

  for value, result in successes:
    LOGGER.info('%s=%s', value, result)
  if errors:
    LOGGER.error('Didn\'t understand %s', Join.join_words(errors))

GET_HELP = """
  Prints one or more configuration variables.

Examples:
  config.get speed
  config.get audio.input.enabled audio.output.enabled
"""

CommandRegistry.register(get_config, 'get', GET_HELP)
