from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Settings

def display(callback):
  use_pi3d = Settings.get('pi3d', 'enable')
  if use_pi3d:
    from echomesh.graphics.Pi3dDisplay import Pi3dDisplay
    return Pi3dDisplay()

  else:
    from echomesh.graphics.CDisplay import CDisplay
    return CDisplay(callback)
