from __future__ import absolute_import, division, print_function, unicode_literals

class Formatted(object):
    """A base class for an object that is represented by formatting its own
    __dict__.  To use, derive from this class, then set a FORMAT member to be a
    string suitable for use in format()."""

    FORMAT = ''
    FORMAT_MEMBERS = []
    FORMAT_WITH_CLASS = True

    def _formatted(self):
        if not self.FORMAT:
            self.FORMAT = ' '.join(
                '%s={%s}' % (m, m) for m in self.FORMAT_MEMBERS)
        return self.FORMAT.format(**self.__dict__)

    def __str__(self):
        return repr(self) if self.FORMAT_WITH_CLASS else self._formatted()

    def __repr__(self):
        cl = self.__class__
        return '%s.%s(%s)' % (cl.__module__, cl.__name__, self._formatted())
