"""
>>> wr = WeightedRandom([None])
>>> wr.select()
0

>>> wr = WeightedRandom([1])
>>> wr.select()
0

>>> wr = WeightedRandom([None, None])
>>> wr.select(0.4)
0

>>> wr.select(0.6)
1

>>> wr = WeightedRandom([1, None])
>>> wr.select(0.4)
0

>>> wr.select(0.6)
1

>>> wr = WeightedRandom([1, 3])
>>> wr.select(0.2)
0

>>> wr.select(0.25)
1

>>> wr.select(0.4)
1

>>> wr.select(0.6)
1

>>> v = [1, 4, 9, 25]
>>> s = 1 / sum(v)
>>> wr = WeightedRandom(v)
>>> wr.select(0)
0

>>> wr.select(s)
1

>>> wr.select(5 * s)
2

>>> wr.select(14 * s)
3

>>> wr.select(39 * s)
4

>>> wr = WeightedRandom([1, None, 9, None, 20])
>>> s = 1 / 50
>>> wr.select(s / 2)
0

>>> wr.select(s)
1

>>> wr.select(10 * s)
1

>>> wr.select(11 * s)
2

>>> wr.select(19 * s)
2

>>> wr.select(20 * s)
3

>>> wr.select(29 * s)
3

>>> wr.select(30 * s)
4

>>> wr.select(50 * s)
5

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math.WeightedRandom import WeightedRandom

