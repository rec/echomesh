"""
# >>> scene = Scene.scene(None, TEST_DATA)

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Scene
from echomesh.base import Yaml

TEST_DATA = Yaml.decode_one("""
  type: insert
  offset: 5
  scene:
    type: spread
    begin: red
    end: white
    steps: 10
  """)

if __name__ == '__main__':
  import doctest
  doctest.testmod()
