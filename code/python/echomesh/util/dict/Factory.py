from __future__ import absolute_import, division, print_function, unicode_literals

class Factory(dict):
    def __init__(self, factory, *args, **kwds):
        super(Factory, self).__init__(*args, **kwds)
        self.factory = factory

    def __missing__(self, key):
        value = self.factory(key)
        self[key] = value
        return value

    def __repr__(self):
        rep = super(Factory, self).__repr__()
        return 'Factory(%s, %s)' % (self.factory, rep)
