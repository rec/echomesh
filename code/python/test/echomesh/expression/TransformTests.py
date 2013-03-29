"""
>>> do_test(Transform.IDENTITY)
>>> do_test(Transform.SQUARE)
>>> do_test(Transform.power(3))
>>> do_test(Transform.SINE)
>>> do_test(Transform.EXP)

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import Transform

VALUES = 0, 1, 0.5, 1 / 3, 2 / 3

TINY = 0.000001

def near(x, y):
  assert abs(x - y) < TINY, '%s != %s' % (x, y)

def do_test(tr):
  s, t = tr
  near(s(0), 0)
  near(t(0), 0)
  near(s(1), 1)
  near(t(1), 1)

  for v in VALUES:
    near(v, s(t(v)))
    near(v, t(s(v)))
