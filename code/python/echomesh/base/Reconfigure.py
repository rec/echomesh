from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import CommandFile
from echomesh.base import MergeConfig
from echomesh.base import Name
from echomesh.base import Path

def _make(name, tags, project, show_error, prompt):
  Name.set_name(name)
  Name.set_tags(tags)
  Path.set_project_path(project_path=project, show_error=show_error)

  CommandFile.compute_command_path()
  return MergeConfig.MergeConfig()

def reconfigure():
  # Read a configuration file with a given name, tags, and project.
  # First, make a config with the default information.
  merge_config = _make(None, [], None, False, False)

  # Now, use the name, tags and project to get the correct configuration.
  get = merge_config.config.get

  name = get('name') or Name.lookup(get('map', {}).get('name', {}))
  tags = get('tag') or Name.lookup(get('map', {}).get('tag', {})) or []
  project = get('project')

  if not isinstance(tags, (list, tuple)):
    tags = [tags]

  return _make(name, tags, project, True, prompt=not get('autostart'))
