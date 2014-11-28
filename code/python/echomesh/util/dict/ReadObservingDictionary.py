from __future__ import absolute_import, division, print_function, unicode_literals

class ReadObservingDictionary(dict):
    def __init__(self, *args, **kwds):
        super(ReadObservingDictionary, self).__init__(*args, **kwds)
        self.read = set()

    def __getitem__(self, key):
        self.read.add(key)
        return super(ReadObservingDictionary, self).__getitem__(key)

    def get(self, key, default=None):
        self.read.add(key)
        return super(ReadObservingDictionary, self).get(key, default)

    def unread(self):
        return set(self.keys()) - self.read
