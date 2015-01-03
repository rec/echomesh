from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from weakref import WeakSet

except:
    from weakrefset import WeakSet

from echomesh.base import DataFile
from echomesh.base import Join
from echomesh.base import MergeSettings
from echomesh.base import Name
from echomesh.base import Path

_MERGE_SETTINGS = None
_CLIENTS = WeakSet()
_NONE = object()
_ARGS = []

def read_settings(args=None):
    global _ARGS
    if args is not None:
        _ARGS = args

    def _make(name, tags, project, show_error):
        Name.set_name(name)
        Name.set_tags(tags)
        Path.set_project_path(project_path=project, show_error=show_error)

        DataFile.compute_command_path(force=True)
        return MergeSettings.MergeSettings(args)

    # Read a settings file with a given name, tags, and project.
    # First, make a settings with the default information.
    merge_settings = _make(None, [], None, False)

    # Now, use the name, tags and project to get the correct configuration.
    get = merge_settings.settings.get

    name = get('name') or Name.lookup(get('map', {}).get('name', {}))
    tags = get('tag') or Name.lookup(get('map', {}).get('tag', {})) or []
    project = get('project')

    if not isinstance(tags, (list, tuple)):
        tags = [tags]

    prompt = not get('execution', 'autostart')
    global MERGE_SETTINGS
    MERGE_SETTINGS = _make(name, tags, project, prompt)

def add_client(client):
    if not client in _CLIENTS:
        _CLIENTS.add(client)
        client.settings_update(get)

def update_clients():
    for c in _CLIENTS:
        c.settings_update(get)

def get_settings():
    if not MERGE_SETTINGS:
        read_settings()
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
