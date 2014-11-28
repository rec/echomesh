from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Settings

class SettingsValues(object):
    def __init__(self,
                 settings=None,
                 values=None,
                 add_client=Settings.add_client,
                 update_callback=None):
        self.update_callback = update_callback
        for k, v in (values or {}).items():
            if v is not None:
                assert not hasattr(self, k)
                setattr(self, k, v)

        self._settings = {}
        for k, v in (settings or {}).items():
            if not (v is None or hasattr(self, k)):
                self._settings[k] = v.split('.')

        self.add_client = lambda: add_client(self)

    def settings_update(self, get):
        for k, v in self._settings.items():
            setattr(self, k, get(*v))
        self.update_callback and self.update_callback()
