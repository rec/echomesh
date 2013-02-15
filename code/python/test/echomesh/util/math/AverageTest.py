"""
>>> list(Average.average(range(8), grouped_window=2))
[0.5, 2.5, 4.5, 6.5]

>>> list(Average.average(range(8), grouped_window=2, moving_window=2))
[1.5, 3.5, 5.5]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.math import Average
