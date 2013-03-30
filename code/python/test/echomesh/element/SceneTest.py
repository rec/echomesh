"""
>>> scene = Scene.scene(None, TEST_DATA)

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Yaml
from echomesh.element import Scene

TEST_DATA = Yaml.decode_one("""
type: insert
offset: 5
scene:
  type: spread
  begin: red
  end: white
  steps: 10
""")
