from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.command import Register
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def get_config(_, value, *more):
  errors = []
  successes = []
  for v in (value,) + more:
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

Register.register(get_config, 'get', GET_HELP)
