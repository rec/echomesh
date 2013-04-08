from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Enum
from echomesh.base import Yaml

ARGS = []

_LEFT = '{[('
_RIGHT_TO_LEFT = dict(zip('}])', _LEFT))

def set_arguments(argv):
  global ARGS
  ARGS[:] = split_args(argv[1:])

# Assignment looks like this:
#  some.name.here = "123"  other.name.here = [1, 2]

State = Enum.enum(
  'BEFORE_ADDRESS',
  'IN_ADDRESS',
  'BEFORE_EQUALS',
  'BEFORE_VALUE',
  'IN_VALUE',
  )

# Handles quotation marks, brackets, etc.
def split_args(s):
  if not isinstance(s, six.string_types):
    s = ' '.join(s)
  results = []
  in_quotes = False
  backslashed = False
  state = State.BEFORE_ADDRESS
  bracket_stack = []
  address = []
  value = []

  for col, ch in enumerate(s):
    def error(s):
      raise Exception('At column %d: %s.' % (1 + col, s))
    perhaps_done = False

    if state is State.BEFORE_ADDRESS:
      if ch.isalpha():
        address.append(ch)
        state = State.IN_ADDRESS
      elif not ch.isspace():
        error('Expected a letter, not "%s"' % ch)
      continue

    if state is State.IN_ADDRESS:
      if ch.isalpha() or ch == '.':
        address.append(ch)
      elif ch.isspace():
        state = State.BEFORE_EQUALS
      elif ch == '=':
        state = State.BEFORE_VALUE
      continue

    if state is State.BEFORE_EQUALS:
      if ch == '=':
        state = State.BEFORE_VALUE
      elif not ch.isspace():
        error('Expected "=", not "%s"' % ch)
      continue

    if state is State.BEFORE_VALUE:
      if ch.isspace():
        continue
      state = State.IN_VALUE

    if backslashed:
      backslashed = False

    elif ch == '\\':
      backslashed = True
      continue

    elif ch == '"':
      if in_quotes:
        in_quotes = False
        perhaps_done = True
      else:
        in_quotes = True

    elif in_quotes:
      pass

    elif ch.isspace():
      if not bracket_stack:
        perhaps_done = True

    elif ch in _LEFT:
      bracket_stack.append(ch)

    elif ch in _RIGHT_TO_LEFT:
      left = _RIGHT_TO_LEFT[ch]
      if not bracket_stack:
        error('Closing %s without opening %s' % (ch, left))
      top = bracket_stack.pop()
      if top != left:
        error('Got closing %s for opening %s' % (left, top))
      perhaps_done = True

    value.append(ch)
    last_time = col == (len(s) - 1)
    if last_time:
      if bracket_stack:
        error('Missing closing brackets for %s' % ''.join(bracket_stack))
      elif in_quotes:
        error('unterminated quotation mark')
    if perhaps_done or last_time:
      if bracket_stack or in_quotes:
        continue
      if address:
        if value:
          val = ''.join(value).strip()
          results.append([''.join(address).strip().split('.'),
                          Yaml.decode_one(val)])
          address = []
          value = []
          state = State.BEFORE_ADDRESS
        else:
          error('empty value for address %s' % address)
      elif value:
        error('empty address for value %s' % value)

  if value:
    error('value was incomplete')
  elif address:
    error('expected to see a value')

  return results
