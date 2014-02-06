from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import DataFile
from echomesh.base import MergeConfig
from echomesh.base import Name
from echomesh.base import Path

def _make(name, tags, project, show_error, args):
  Name.set_name(name)
  Name.set_tags(tags)
  Path.set_project_path(project_path=project, show_error=show_error)

  DataFile.compute_command_path(force=True)
  return MergeConfig.MergeConfig(args)

def reconfigure(args):
  # Read a configuration file with a given name, tags, and project.
  # First, make a config with the default information.
  merge_config = _make(None, [], None, False, args)

  # Now, use the name, tags and project to get the correct configuration.
  get = merge_config.config.get

  name = get('name') or Name.lookup(get('map', {}).get('name', {}))
  tags = get('tag') or Name.lookup(get('map', {}).get('tag', {})) or []
  project = get('project')

  if not isinstance(tags, (list, tuple)):
    tags = [tags]

  prompt = not get('autostart')
  return _make(name, tags, project, prompt, args)
