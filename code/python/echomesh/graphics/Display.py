from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config

def display():
    if Config.get('load_module', 'pi3d'):
      from echomesh.graphics.Pi3dDisplay import Pi3dDisplay
      return Pi3dDisplay()


