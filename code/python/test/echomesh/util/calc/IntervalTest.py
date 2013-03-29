"""
>>> interval()
(inf, 0, inf, 1)

>>> interval(10)
(10, 0, 9, 1)

>>> interval(count=10)
(10, 0, 9, 1)

>>> interval(begin=10)
(inf, 10, inf, 1)

>>> interval(end=10)
(11, 0, 10, 1)

>>> interval(begin=10, end=15)
(6, 10, 15, 1)

>>> interval(begin=10, count=5)
(5, 10, 14, 1)

>>> interval(end=10, count=5)
(5, 6, 10, 1)

>>> interval(begin=10, end=5)
(6, 10, 5, -1)

>>> interval(begin=10, count=3, skip=-2)
(3, 10, 6, -2)

>>> interval(begin=10, end=3, skip=-2)
(4, 10, 3, -2)

>>> interval(begin=10, end=3, count=3)
(3, 10, 3, -2)



"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math.Interval import interval

