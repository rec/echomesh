from __future__ import absolute_import, division, print_function, unicode_literals

import six

def log_scale(value, scale, exponent):
  return exponent ** (value / scale)

def make_log(scale, exponent):
  def log_unit(x):
    return log_scale(x, scale, exponent)
  return log_unit

def make_scale(scale):
  def scale_unit(x):
    return x * scale
  return scale_unit

def inverse_scale(scale=1.0):
  def inverse_scale_unit(x):
    return 1.0 / (scale * x)
  return inverse_scale_unit

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
  keys = six.iterkeys(UNITS_SOURCE)
  return separator + ('\n' + separator).join((', '.join(k) for k in keys))

UNITS = {}

for _keys, _v in six.iteritems(UNITS_SOURCE):
  for _k in _keys:
    UNITS[_k] = _v

INFINITY = float('inf')
