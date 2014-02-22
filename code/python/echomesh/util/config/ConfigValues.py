from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config

class ConfigValues(object):
  def __init__(self, configs=None, values=None, add_client=Config.add_client,
               update_callback=None):
    self.update_callback = update_callback
    for k, v in (values or {}).items():
      if v is not None:
        assert not hasattr(self, k)
        setattr(self, k, v)

    self._configs = {}
    for k, v in (configs or {}).items():
      if not (v is None or hasattr(self, k)):
        self._configs[k] = v.split('.')

    self.add_client = lambda: add_client(self)

  def config_update(self, get):
    for k, v in self._configs.items():
      setattr(self, k, get(*v))
    self.update_callback and self.update_callback()


