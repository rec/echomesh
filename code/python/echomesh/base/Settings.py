from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from weakref import WeakSet

except:
    from weakrefset import WeakSet

from echomesh.base import Join
from echomesh.base import Reconfigure

_MERGE_SETTINGS = None
_CLIENTS = WeakSet()
_NONE = object()
_ARGS = []

def reconfigure(args=None):
    global _ARGS, MERGE_SETTINGS
    if args:
        _ARGS = args
    MERGE_SETTINGS = Reconfigure.reconfigure(_ARGS)

def add_client(client):
    if not client in _CLIENTS:
        _CLIENTS.add(client)
        client.settings_update(get)

def update_clients():
    for c in _CLIENTS:
        c.settings_update(get)

def get_settings():
    if not MERGE_SETTINGS:
        reconfigure()
    return MERGE_SETTINGS.settings

def get(*parts):
    settings = get_settings()
    for part in parts:
        try:
            settings = settings[part]
        except KeyError:
            raise Exception('Couldn\'t find settings "%s"' % '.'.join(parts))
        except AttributeError:
            raise Exception("Reached leaf settings for %s: %s" %
                            ('.'.join(parts), settings))
    return settings

def assign(values):
    return MERGE_SETTINGS.assign(values)

# Automatically save any changed variables on exit.
def save(log=True):
    if get('execution', 'autosave'):
        files = MERGE_SETTINGS.save()
        if log and files:
            print(
                'Settings automatically saved to', Join.join_file_names(files))
        return files

def assignments():
    return MERGE_SETTINGS.assignments()

def has_changes():
    return MERGE_SETTINGS.has_changes()

def get_changes():
    return MERGE_SETTINGS.get_changes()
