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

>>> Units.convert(12)
12

>>> Units.convert('12')
12

>>> Units.convert('12 db')
3.9810717055349722

>>> Units.convert('12dB')
3.9810717055349722

>>> Units.convert('10 semitones')
1.7817974362806785

>>> Units.convert('-1 semitone')
0.9438743126816935

>>> Units.convert('50 cents')
1.029302236643492

>>> Units.convert('50 cent')
1.029302236643492

>>> Units.convert('-1.034E+2 semitones')
0.0025475626362608667

>>> Units.convert('-103.4 semitones')
0.0025475626362608667

>>> Units.convert('10ms')
0.01

>>> Units.convert_time('0')

>>> Units.convert_time('0:0')

>>> Units.convert_time('0:00')
0

>>> Units.convert_time('0:01')
1

>>> Units.convert_time('0:01:00')
60

>>> Units.convert_time('0:01:00.12')
60.12

>>> Units.convert_time('1:01:00.12')
3660.12

>>> Units.convert('13 + 12 ms')
0.025

>>> Units.convert('1/2sec')
0.5

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math import Average
from echomesh.util.math import Envelope
from echomesh.util.math import Units
from echomesh.util.math.WeightedRandom import WeightedRandom

