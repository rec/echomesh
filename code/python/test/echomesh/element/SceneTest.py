"""
>>> scene = Scene.scene(None, TEST_DATA)
>>> scene.evaluate()
array([[ 255.        ,    0.        ,    0.        ],
       [ 255.        ,   28.33333333,   28.33333333],
       [ 255.        ,   56.66666667,   56.66666667],
       [ 255.        ,   85.        ,   85.        ],
       [ 255.        ,  113.33333333,  113.33333333],
       [ 255.        ,  141.66666667,  141.66666667],
       [ 255.        ,  170.        ,  170.        ],
       [ 255.        ,  198.33333333,  198.33333333],
       [ 255.        ,  226.66666667,  226.66666667],
       [ 255.        ,  255.        ,  255.        ]])

>>> scene = Scene.scene(None, TEST_DATA2)
>>> scene.evaluate()
[None, None, None, None, None, array([ 255.,    0.,    0.]), array([ 255.        ,   28.33333333,   28.33333333]), array([ 255.        ,   56.66666667,   56.66666667]), array([ 255.,   85.,   85.]), array([ 255.        ,  113.33333333,  113.33333333]), array([ 255.        ,  141.66666667,  141.66666667]), array([ 255.,  170.,  170.]), array([ 255.        ,  198.33333333,  198.33333333]), array([ 255.        ,  226.66666667,  226.66666667]), array([ 255.,  255.,  255.])]

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
