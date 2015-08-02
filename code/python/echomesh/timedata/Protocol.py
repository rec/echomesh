from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import six

from echomesh.util import Log

LOGGER = Log.logger(__name__)


def is_tag(t):
    """A tag is a string of length greater than 1 starting with # but not ##."""
    return len(t) > 1 and t.startswith('#') and not t.startswith('##') and t

def pop_tag(data):
    """If the first value in this list is a tag, pop and return it."""
    if data and is_tag(data[0]):
        return data.pop(0)


class Protocol(object):
    DICTIONARY = {}

    def __init__(self, tag, length=0, filler=0, **kwds):
        assert tag[0] == '#'
        assert tag not in self.DICTIONARY
        self.tag = tag
        self.kwds = kwds
        self.DICTIONARY[tag] = self
        self.length = length

    def compress(self, tag_changed, new_data, old_data):
        result = [self.name] if tag_changed else []
        result += self._compress(list(new_data), old_data)
        old_data[:] = new_data
        return result

    def expand(self, tag_changed, new_data, old_data):
        if self.length > len(old_data):
            fill = [self.filler] * (self.length - len(old_data))
            old_data = self._fill(old_data, fill)
        old_data[:] = self._expand(new_data, old_data)
        return [self.name] + old_data

    def _compress(self, new_data, old_data):
        return new_data

    def _expand(self, new_data, old_data):
        return new_data

    def _compress_index(self, new_data, old_data, index):
        assert len(new_data) == len(old_data)
        while new_data and new_data[index] == old_data[index]:
            new_data.pop(index)
            old_data.pop(index)
        return new_data

    def _fill(self, old_data, fill):
        return old_data + fill


class RightProtocol(Protocol):
    # When we expand, we fill in on the right side.
    def _expand(self, new_data, old_data):
        if len(new_data) < len(old_data):
            new_data += old_data[len(new_data):]
        return new_data

    def _compress(self, new_data, old_data):
        return self._compress_index(new_data, old_data, -1)


class LeftProtocol(Protocol):
    # When we expand, we fill in on the left side.
    def _expand(self, new_data, old_data):
        if len(new_data) < len(old_data):
            new_data = old_data[:len(old_data) - len(new_data)] + new_data
        return new_data

    def _compress(self, new_data, old_data):
        return self._compress_index(new_data, old_data, 0)

    def _fill(self, old_data, fill):
        return fill + old_data


# NONE is a special empty protocol with an empty tag.
NONE = Protocol('#')
MIDI = LeftProtocol('#midi', 4)

class Compander(object):
    def __init__(self, protocol, protocol_dict, method_name):
        self.state_dict = {}
        self.protocol_dict = protocol_dict
        self.method_name = method_name
        self._set_tag(protocol.tag)

    def _set_tag(self, tag):
        state = self.state_dict.get(tag)
        if state:
            self.protocol, self.data = state
        else:
            self.protocol = self.protocol_dict.get(tag, NONE)
            self.data = []
            self.state[tag] = self.protocol, self.data
        self.method = getattr(self.protocol, self.method_name)

    def filter(self, data):
        tag = pop_tag(*data)
        tag_changed = tag and tag != self.protocol.tag
        if tag_changed:
            self._set_tag(tag)
        return self.method(tag_changed, data, self.data)

def compresser(protocol=NONE, protocol_dict=Protocol.DICTIONARY):
    return Compander(protocol, protocol, 'compress')

def expander(protocol=NONE, protocol_dict=Protocol.DICTIONARY):
    return Compander(protocol, protocol, 'expand')
