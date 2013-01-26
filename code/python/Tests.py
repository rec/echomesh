"""
>>> env = Envelope.Envelope([[0, 5.0], [1, 10.0], [2, 20.0]])

>>> env.interpolate(-1)
5.0

>>> env.interpolate(0)
5.0

>>> env.interpolate(0.5)
7.5

>>> env.interpolate(1)
10.0

>>> env.interpolate(1.5)
15.0

>>> env.interpolate(2)
20.0

>>> env.interpolate(3)
20.0

>>> env2 = Envelope.Envelope([[0, [5.0, 50.0]], [1, [10.0, 100.0]], [2, [20.0, 200.0]]])

>>> env2.interpolate(-1)
[5.0, 50.0]

>>> env2.interpolate(0)
[5.0, 50.0]

>>> env2.interpolate(0.5)
[7.5, 75.0]

>>> env2.interpolate(1)
[10.0, 100.0]

>>> env2.interpolate(1.5)
[15.0, 150.0]

>>> env2.interpolate(2)
[20.0, 200.0]

>>> env2.interpolate(3)
[20.0, 200.0]

>>> list(Average.average(range(8), moving_window=2))
[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]

>>> list(Average.average(range(8), grouped_window=2))
[0.5, 2.5, 4.5, 6.5]

>>> list(Average.average(range(8), grouped_window=2, moving_window=2))
[1.5, 3.5, 5.5]

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

>> resolve_scope('abc')

>> resolve_scope('local')



"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base.CommandFile import resolve_scope
from echomesh.base import Merge
from echomesh.util.math import Average
from echomesh.util.math import Envelope
from echomesh.util.math.WeightedRandom import WeightedRandom

if __name__ == "__main__":
  import doctest
  doctest.testmod()
