from __future__ import absolute_import, division, print_function, unicode_literals

import re
import six

from echomesh.expression.Units import INFINITY

INFINITY = float('inf')
NAMES_FOR_INFINITY = set(('inf', 'infinite', 'infinity'))

_TIME = re.compile(r'( ( \d+ ) : )? ( \d+ ) : ( \d \d (\. ( \d* ) )? )', re.X)
_HEX = re.compile(r'( 0x [0-9a-f]+ )', re.X)

def convert_time(t, assume_minutes=True):
  time_match = _TIME.match(t)
  if time_match:
    hours, minutes, seconds = time_match.group(2, 3, 4)
    float_seconds = '.' in seconds
    seconds = (float if float_seconds else int)(seconds)
    minutes = int(minutes)

    if assume_minutes or float_seconds or (hours is not None):
      hours = int(hours or '0')
    else:
      hours, minutes, seconds = minutes, seconds, 0

    if seconds >= 60:
      raise Exception('Bad seconds field in time %s', t)
    if hours:
      if minutes >= 60:
        raise Exception('Bad minutes field in time %s', t)

    return 3600 * hours + 60 * minutes + seconds

def convert_number(expression, assume_minutes):
  if expression and isinstance(expression, six.string_types):
    expression = expression.strip().lower()
    if expression in NAMES_FOR_INFINITY:
      return INFINITY
    else:
      return convert_time(expression, assume_minutes)
  else:
    return expression
