from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Enum
from echomesh.base import Yaml

ARGS = []
_ARGUMENT_ERROR = """
ERROR: Didn't understand arguments to echomesh: "%s".

echomesh needs to be called with arguments looking like "name=value".

Examples:
  echomesh
  echomesh debug=true
  echomesh audio.input.enable=false light.enable=false
"""

_LEFT = '{[('
_RIGHT_TO_LEFT = dict(zip('}])', _LEFT))

def set_arguments(argv):
  global ARGS
  try:
    ARGS[:] = split_args(''.join(argv[1:]))
    return True
  except:
    print(_ARGUMENT_ERROR % ' '.join(argv[1:]))

# Assignment looks like this:
#  some.name.here = "123"  other.name.here = [1, 2]

State = Enum.Enum(
  'BEFORE_ADDRESS',
  'IN_ADDRESS',
  'BEFORE_EQUALS',
  'BEFORE_VALUE',
  'IN_VALUE',
  )

class _ArgParser(object):
  def split(self, string):
    # if isinstance(s, six.string_types) else ' '.join(s)  # fix
    self.string = string
    self.col = 0
    self.results = []

    self.clear()
    while self.col < len(self.string):
      self.state(self.string[self.col])

    if self.bracket_stack:
      self.error('missing closing brackets in %s' % ''.join(self.bracket_stack))
    elif self.in_quotes:
      self.error('unterminated quotation mark')

    self.add_result()
    return self.results

  def before_address(self, ch):
    if ch.isalpha():
      self.address.append(ch)
      self.state = self.in_address
    elif not ch.isspace():
      self.error('Expected a letter, not "%s"' % ch)
    self.col += 1

  def in_address(self, ch):
    if ch.isalpha() or ch in '._':
      self.address.append(ch)
    elif ch.isspace():
      self.state = self.before_equals
    elif ch == '=':
      self.state = self.before_value
    self.col += 1

  def before_equals(self, ch):
    if ch == '=':
      self.state = self.before_value
    elif not ch.isspace():
      self.value = 'true'
      self.add_result()

    self.col += 1

  def before_value(self, ch):
    if ch.isspace():
      self.col += 1
    else:
      self.state = self.in_value

  def in_value(self, ch):
    self.col += 1
    if self.backslashed:
      self.backslashed = False
      self.value.append(ch)

    elif ch == '\\':
      self.backslashed = True

    elif ch == '"':
      if self.in_quotes:
        self.in_quotes = False
      else:
        self.in_quotes = True

    elif self.in_quotes:
      self.value.append(ch)

    elif ch.isspace():
      if self.bracket_stack:
        self.value.append(ch)
      else:
        self.add_result()

    elif ch in _LEFT:
      self.value.append(ch)
      self.bracket_stack.append(ch)

    elif ch in _RIGHT_TO_LEFT:
      self.value.append(ch)
      left = _RIGHT_TO_LEFT[ch]
      if not self.bracket_stack:
        self.error('Closing %s without opening %s' % (ch, left))
      top = self.bracket_stack.pop()
      if top != left:
        self.error('Got closing %s for opening %s' % (left, top))
      if not self.bracket_stack:
        self.add_result()

    else:
      self.value.append(ch)

  def clear(self):
    self.address = []
    self.value = []
    self.state = self.before_address
    self.in_quotes = False
    self.backslashed = False
    self.bracket_stack = []

  def add_result(self):
    if self.address:
      value = ''.join(self.value or 'true').strip()
      address = ''.join(self.address).strip().split('.')
      self.results.append([address, Yaml.decode_one(value)])
      self.clear()

  def error(self, msg):
    raise Exception('At column %d: %s.' % (self.col, msg))

def split_args(s):
  return _ArgParser().split(s)

# Handles quotation marks, brackets, etc.
def old_split_args(s):
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
      print('!!! ??', s)
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
      if ch.isalpha() or ch in '._':
        address.append(ch)
      elif ch.isspace():
        state = State.BEFORE_EQUALS
      elif ch == '=':
        state = State.BEFORE_VALUE
      continue

    if state is State.BEFORE_EQUALS:
      if ch == '=':
        state = State.BEFORE_VALUE
      elif ch.isspace():
        continue
      else:
        value = 'true'
        perhaps_done = True

    if state is State.BEFORE_VALUE:
      if ch.isspace():
        continue
      else:
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
      print('!!! last_time !!!')
      if bracket_stack:
        error('Missing closing brackets for %s' % ''.join(bracket_stack))
      elif in_quotes:
        error('unterminated quotation mark')
    if perhaps_done or last_time:
      print('!!! 1 !!!')
      if bracket_stack or in_quotes:
        continue
      if address:
        print('!!! 2 !!!')
        if last_time:
          value = value or 'true'
        if value:
          print('!!! 3 !!!')
          val = ''.join(value).strip()
          results.append([''.join(address).strip().split('.'),
                          Yaml.decode_one(val)])
          address = []
          value = []
        else:
          print('!!! 4 !!!')
          error('empty value for address %s' % address)
        state = State.BEFORE_ADDRESS
      elif value:
        print('!!! 5 !!!')
        error('empty address for value %s' % value)
        state = State.BEFORE_ADDRESS

  if value:
    error('value was incomplete')
  elif address:
    error('expected to see a value')

  return results
