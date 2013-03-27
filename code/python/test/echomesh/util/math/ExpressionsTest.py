"""
>>> evaluate('2+2')
4

>>> evaluate('2+sin(0)')
2.0

>> evaluate('2 + trunc(1.2)')
3

>> evaluate('-cos(0)')
-1
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math.Expressions import evaluate

