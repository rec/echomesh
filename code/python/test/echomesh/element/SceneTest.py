"""
>>> scene = Scene.scene(None, TEST_DATA)
>>> scene.evaluate()
array([[ 1.        ,  0.        ,  0.        ],
       [ 1.        ,  0.11111111,  0.11111111],
       [ 1.        ,  0.22222222,  0.22222222],
       [ 1.        ,  0.33333333,  0.33333333],
       [ 1.        ,  0.44444444,  0.44444444],
       [ 1.        ,  0.55555556,  0.55555556],
       [ 1.        ,  0.66666667,  0.66666667],
       [ 1.        ,  0.77777778,  0.77777778],
       [ 1.        ,  0.88888889,  0.88888889],
       [ 1.        ,  1.        ,  1.        ]])

>>> scene = Scene.scene(None, TEST_DATA2)
>>> scene.evaluate()
[None, None, None, None, None, array([ 1.,  0.,  0.]), array([ 1.        ,  0.11111111,  0.11111111]), array([ 1.        ,  0.22222222,  0.22222222]), array([ 1.        ,  0.33333333,  0.33333333]), array([ 1.        ,  0.44444444,  0.44444444]), array([ 1.        ,  0.55555556,  0.55555556]), array([ 1.        ,  0.66666667,  0.66666667]), array([ 1.        ,  0.77777778,  0.77777778]), array([ 1.        ,  0.88888889,  0.88888889]), array([ 1.,  1.,  1.])]

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
