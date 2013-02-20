from __future__ import absolute_import, division, print_function, unicode_literals

import re

import six
from pyparsing import Expressions

_TIME = re.compile(r'( ( \d+ ) : )? ( \d+ ) : ( \d \d (\. ( \d* ) )? )', re.X)
_HEX = re.compile(r'( 0x [0-9a-f]+ )', re.X)
_ANY_UNIT = re.compile(r'( .*? ) \s* ( [a-z%]* ) \s* $', re.X)

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

def list_units(separator='\n  '):
  keys = UNITS_SOURCE.iterkeys()
  return separator + separator.join((', '.join(k) for k in keys))

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

def convert_number(number):
  if not number.startswith('0x'):
    return Expressions.evaluate(number)

  # A hex number, must be integer.
  hex_match = _HEX.match(number)
  if not hex_match:
    raise Exception("Can't understand hex number %s" % number)
  return int(hex_match.groups()[0], 16)

def convert(number, assume_minutes=True):
  if not (number and isinstance(number, six.string_types)):
    return number
  number = number.strip()

  if number in ['infinite', 'infinity']:
    return float('inf')

  t = convert_time(number, assume_minutes)
  if t is not None:
    return t

  number = number.lower()
  unit_match = _ANY_UNIT.match(number)

  if unit_match:
    prefix, unit = unit_match.groups()
    unit_converter = UNITS.get(unit)
    if unit_converter:
      return unit_converter(convert_number(prefix))

  return convert_number(number)

