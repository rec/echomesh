from __future__ import absolute_import, division, print_function, unicode_literals

import numpy
import re

from pyparsing import expressions
from python import six

_UNIT = r'\s* ( [a-z]* ) \s* $'
_NUMBER = re.compile(r'( [+-]? \d* (\.?) \d* ( e [+-]? \d+ )? )' + _UNIT, re.X)
_TIME = re.compile(r'( ( \d+ ) : ) ( \d \d? ) : ( \d \d )', re.X)
_HEX = re.compile(r'( 0x [0-9a-f]+ )' + _UNIT, re.X)
_ANY_UNIT = re.compile(r'( .* )' + _UNIT, re.X)

def log_scale(value, scale, exponent):
  return exponent ** (value / scale)

def make_log(scale, exponent):
  return lambda number: log_scale(number, scale, exponent)

_UNITS = {
  ('cents', 'cent'): make_log(1200, 2),
  ('db', 'decibels', 'decibel'): make_log(20, 10),
  ('min', 'minutes', 'minute'): lambda ms: ms / 1000,
  ('ms', 'milliseconds', 'millisecond'): lambda ms: ms / 1000,
  ('semitones', 'semitone'): make_log(12, 2),
}

def _unit_lookup(units):
  result = {}
  for keys, v in units.iteritems():
    for k in keys:
      result[k] = v
  return result

_UNIT_LOOKUP = _unit_lookup(_UNITS)


def convert(number):
  if not isinstance(number, six.string_types):
    return number
  number = number.lower()
  unit_match = _ANY_UNIT.match(number)
  if unit_match:
    number, unit = unit_match.groups()
  else:
    unit = ''

  hex_match = _HEX.match(number)
  if number.startswith('0x'):
    # A hex number, must be integer.
    hex_match = _HEX.match(number)
    if not hex_match:
      raise Exception("Can't understand hex number %s" % number)
    number = int(hex_match.groups()[0], 16)
  else:


    # Not hex, might be an integer or a float.
    m = _NUMBER.match(number)
    if not m:
      raise Exception("Can't understand number %s" % number)

    number, period, exponent, unit = m.groups()
    is_float = period or exponent
    number = (is_float and float or int)(number)

  if unit:
    unit_converter = _UNIT_LOOKUP.get(unit)
    if unit_converter:
      number = unit_converter(number)
    else:
      raise Exception("Didn't understand unit '%s' in number '%s'" %
                      (unit, number))

  return number



def _to_number(number):
  if number.startswith('0x'):
    # A hex number, must be integer.
    m = _HEX.match(number)
    if not m:
      raise Exception("Can't understand hex number %s" % number)
    number, unit = m.groups()
    return int(number, 16)

  else:

    # Not hex, might be an integer or a float.
    m = _NUMBER.match(number)
    if not m:
      raise Exception("Can't understand number %s" % number)

    number, period, exponent, unit = m.groups()
    is_float = period or exponent
    number = (is_float and float or int)(number)

def convert(number):
  if not isinstance(number, six.string_types):
    return number

  number = number.lower()
  if number.startswith('0x'):
    # A hex number, must be integer.
    m = _HEX.match(number)
    if not m:
      raise Exception("Can't understand hex number %s" % number)
    number, unit = m.groups()
    number = int(number, 16)

  else:
    # Not hex, might be an integer or a float.
    m = _NUMBER.match(number)
    if not m:
      raise Exception("Can't understand number %s" % number)

    number, period, exponent, unit = m.groups()
    is_float = period or exponent
    number = (is_float and float or int)(number)

  if unit:
    unit_converter = _UNIT_LOOKUP.get(unit)
    if unit_converter:
      number = unit_converter(number)
    else:
      raise Exception("Didn't understand unit '%s' in number '%s'" %
                      (unit, number))

  return number
