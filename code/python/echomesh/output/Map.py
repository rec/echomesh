from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Map(Output):
    def __init__(self, map=None, filter=False, **description):
        super(Map, self).__init__()
        self.filter = filter
        if map is None:
            LOGGER.error('No map in output Map')
        self.map = map or {}
        reverse = {}
        length = -1

        for key, value in self.map.copy().items():
            if not isinstance(value, (list, tuple)):
                value = [value]
                self.map[key] = value
            length = max(length, *value)
            for v in value:
                reverse.setdefault(v, []).append(key)
        self.length = 1 + length

        errors = []
        for key, value in reverse.items():
            if len(value) > 1:
                parts = ', '.join(str(v) for v in value)
                errors.append('(%s) -> %s' % (parts, key))
        if errors:
            LOGGER.error('Map output: multiple keys mapped onto one: %s',
                         ' '.join(errors))

        self.finish_construction(description)

    def emit_output(self, data):
        old_data, data = data, [None] * max(self.length, len(data))
        parts = []
        for i, x in enumerate(old_data):
            for s in self.map.get(i, []):
                data[s] = x

        if not self.filter:
            for i, x in enumerate(old_data):
                if data[i] is None:
                    data[i] = x

        super(Map, self).emit_output(data)
