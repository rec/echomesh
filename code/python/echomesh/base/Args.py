from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Yaml

_LEFT = '{[('
_RIGHT_TO_LEFT = dict(zip('}])', _LEFT))

# Assignment looks like this:
#  some.name.here = "123"  other.name.here = [1, 2]

class _ArgParser(object):
    def split(self, string):
        self.string = string
        self.col = 0
        self.results = []

        self.clear()
        while self.col < len(self.string):
            self.state(self.string[self.col])

        if self.bracket_stack:
            self.error('missing closing brackets in %s' %
                       ''.join(self.bracket_stack))
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
        if ch.isalnum() or ch in '._':
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
            return

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
            value = ''.join(self.value or 'true')
            address = ''.join(self.address)
            self.results.append([address, Yaml.decode_one(value)])
            self.clear()

    def error(self, msg):
        raise Exception('At column %d: %s.' % (self.col, msg))

def split(s):
    return _ArgParser().split(s)
