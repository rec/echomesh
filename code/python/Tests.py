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

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Merge
from echomesh.util.math import Average
from echomesh.util.math import Envelope

if __name__ == "__main__":
  import doctest
  doctest.testmod()
