from __future__ import absolute_import, division, print_function, unicode_literals

import numpy
import re

from pyparsing import Expressions
from python import six

_TIME = re.compile(r'( ( \d+ ) : )? ( \d+ ) : ( \d \d (\. ( \d* ) )? )', re.X)
_HEX = re.compile(r'( 0x [0-9a-f]+ )', re.X)
_ANY_UNIT = re.compile(r'( .*? ) \s* ( [a-z]* ) \s* $', re.X)

def log_scale(value, scale, exponent):
  return exponent ** (value / scale)

def make_log(scale, exponent):
  return lambda number: log_scale(number, scale, exponent)

_UNITS_SOURCE = {
  ('cents', 'cent'): make_log(1200, 2),
  ('db', 'decibels', 'decibel'): make_log(20, 10),
  ('min', 'minutes', 'minute'): lambda ms: ms / 1000,
  ('ms', 'milliseconds', 'millisecond'): lambda ms: ms / 1000,
  ('semitones', 'semitone'): make_log(12, 2),
}

_UNITS = {}

for _keys, _v in _UNITS_SOURCE.iteritems():
  for _k in _keys:
    _UNITS[_k] = _v

def convert_time(t):
  time_match = _TIME.match(t)
  if time_match:
    hours, minutes, seconds = time_match.group(2, 3, 4)
    seconds = (float if '.' in seconds else int)(seconds)
    minutes = int(minutes)
    hours = int(hours or '0')

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

def convert(number):
  if not isinstance(number, six.string_types):
    return number

  t = convert_time(number)
  if t is not None:
    return t

  number = number.lower()
  unit_match = _ANY_UNIT.match(number)

  if unit_match:
    prefix, unit = unit_match.groups()
    unit_converter = _UNITS.get(unit)
    if unit_converter:
      return unit_converter(convert_number(prefix))

  return convert_number(number)

