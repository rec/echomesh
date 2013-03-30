"""
>>> scene = Scene.scene(None, TEST_DATA)
>>> scene.evaluate()
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

sys.path.insert(0, '/development/echomesh/code/python/external')
sys.path.insert(0, '/development/echomesh/code/python')

from echomesh.element import Scene
from echomesh.base import Yaml

TEST_DATA = Yaml.decode_one("""
  type: spread
  begin: red
  end: white
  steps: 10
  """)

TEST_DATA2 = Yaml.decode_one("""
  type: insert
  offset: 5
  scene:
    type: spread
    begin: red
    end: white
    steps: 10
  """)
