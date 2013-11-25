from __future__ import absolute_import, division, print_function, unicode_literals

from math import log

def make_log(scale, base):
  return lambda x: base ** (x / scale), lambda x: scale * log(x) / log(base)

def make_scale(scale):
  return lambda x: x * scale, lambda x: x / scale

def inverse_scale(scale=1.0):
  return lambda x: 1.0 / (scale * x), lambda x: (1.0 * scale) / x

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

def list_units(separator='  '):
  keys = UNITS_SOURCE.keys()
  return separator + ('\n' + separator).join((', '.join(k) for k in keys))

UNITS = {}
INVERSE_UNITS = {}

for _keys, _v in UNITS_SOURCE.items():
  for _k in _keys:
    UNITS[_k], INVERSE_UNITS[_k] = _v

INFINITY = float('inf')
