from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import DataFile
from echomesh.base import MergeSettings
from echomesh.base import Name
from echomesh.base import Path

def reconfigure(args):
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
    return _make(name, tags, project, prompt)
