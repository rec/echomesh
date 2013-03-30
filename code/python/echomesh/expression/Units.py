from __future__ import absolute_import, division, print_function, unicode_literals

import re

import six

from echomesh.expression import RawExpression

def log_scale(value, scale, exponent):
  return exponent ** (value / scale)

def make_log(scale, exponent):
  return lambda x: log_scale(x, scale, exponent)

def make_scale(scale):
  return lambda x: x * scale

def inverse_scale(scale=1.0):
  return lambda x: 1.0 / (scale * x)

UNITS_SOURCE = {
  ('%', 'percent'): make_scale(1 / 100),
  ('cent', 'cents'): make_log(1200, 2),
  ('db', 'decibel', 'decibels'): make_log(20, 10),
  ('cps', 'hz', 'hertz'): inverse_scale(),
  ('khz', 'khertz', 'kilohertz'): inverse_scale(1000),
  ('millisecond', 'milliseconds', 'ms'): make_scale(1 / 1000),
  ('min', 'minute', 'minutes'): make_scale(60),
  ('s', 'seconds', 'second', 'sec'): make_scale(1),
  ('semitone', 'semitones'): make_log(12, 2),
}

INFINITY = float('inf')
NAMES_FOR_INFINITY = set(('inf', 'infinite', 'infinity'))

_TIME = re.compile(r'( ( \d+ ) : )? ( \d+ ) : ( \d \d (\. ( \d* ) )? )', re.X)
_HEX = re.compile(r'( 0x [0-9a-f]+ )', re.X)
_ANY_UNIT = re.compile(r'( .*? (?: \d\.? | \s ) ) ( [a-z%]* ) \s* $', re.X)

def list_units(separator='  '):
  keys = UNITS_SOURCE.iterkeys()
  return separator + ('\n' + separator).join((', '.join(k) for k in keys))

UNITS = {}

for _keys, _v in UNITS_SOURCE.iteritems():
  for _k in _keys:
    UNITS[_k] = _v

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

class UnitExpression(object):
  def __init__(self, expression, assume_minutes=True):
    self.expression = self.value = None
    if expression is not None:
      self.value = convert_number(expression, assume_minutes)
      if self.value is None:
        expression = expression.lower()
        unit_match = _ANY_UNIT.match(expression)

        if unit_match:
          expression, unit = unit_match.groups()
          self.unit_converter = UNITS.get(unit)
        else:
          self.unit_converter = None

        self.expression = RawExpression.RawExpression(expression)

  def evaluate(self, element=None):
    return self(element)

  def __call__(self, element=None):
    if not self.expression:
      return self.value

    val = self.expression(element)
    if self.unit_converter:
      return self.unit_converter(val)
    else:
      return val

  def is_variable(self, element=None):
    return self.expression and self.expression.is_variable(element)

def convert(number, element=None, assume_minutes=True):
  if number is None:
    return number
  return UnitExpression(number, assume_minutes)(element)

def get_config(*parts):
  from echomesh.base import Config
  return convert(Config.get(*parts))

def get_table(table, key, default=None):
  return convert(table.get(key, default))
