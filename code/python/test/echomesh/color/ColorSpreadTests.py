"""
>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 0)
array([], shape=(1, 0, 3), dtype=float64)

>>> ColorSpread.color_spread([1, 0, 0], [0, 0, 1], 6)
array([[[ 1. ,  0. ,  0. ],
        [ 1. ,  0.8,  0. ],
        [ 0.4,  1. ,  0. ],
        [ 0. ,  1. ,  0.4],
        [ 0. ,  0.8,  1. ],
        [ 0. ,  0. ,  1. ]]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6)
array([[[ 1. ,  1. ,  0. ],
        [ 0.6,  1. ,  0. ],
        [ 0.2,  1. ,  0. ],
        [ 0. ,  1. ,  0.2],
        [ 0. ,  1. ,  0.6],
        [ 0. ,  1. ,  1. ]]])

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorSpread
