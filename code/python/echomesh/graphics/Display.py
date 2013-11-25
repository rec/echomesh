from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config

_ERROR = """\
You can't use both pi3d and the C++ visualizer at the same time."""

def display():
  use_pi3d = Config.get('load_module', 'pi3d')
  use_visualizer = Config.get('light', 'visualizer', 'type') == 'cython'
  assert not (use_pi3d and use_visualizer), _ERROR
  if use_pi3d:
    from echomesh.graphics.Pi3dDisplay import Pi3dDisplay
    return Pi3dDisplay()

  if use_visualizer:
    from echomesh.graphics.CDisplay import CDisplay
    return CDisplay()

