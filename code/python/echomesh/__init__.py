try:
  import cechomesh
except ImportError:
  class _NoEntry(object):
    LOADED = False

    def __getattr__(self, name):
      raise AttributeError('Not able to import cechomesh dynamic library.')

  cechomesh = _NoEntry()
