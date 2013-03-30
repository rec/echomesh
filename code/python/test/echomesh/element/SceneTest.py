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

"""
Here's the traceback I'm getting...

  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/runpy.py", line 162, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/doctest.py", line 2731, in <module>
    sys.exit(_test())
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/doctest.py", line 2720, in _test
    m = __import__(filename[:-3])
  File "/development/echomesh/code/python/test/echomesh/element/SceneTest.py", line 8, in <module>
    from echomesh.element import Scene
  File "echomesh/element/Scene.py", line 4, in <module>
ImportError: No module named expression.Expression
"""
