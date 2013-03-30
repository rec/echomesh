"""
>>> ColorConv.rgb_to_hsv([0, 0, 0])
array([[ 0.,  0.,  0.]])

>>> ColorConv.rgb_to_hsv([[0, 0, 0]])
array([[ 0.,  0.,  0.]])

>>> ColorConv.rgb_to_hsv([(1, 1, 1)])
array([[ 0.,  0.,  1.]])

>>> ColorConv.rgb_to_hsv([[1.0, 0, 0], [0, 0, 1.0]])
array([[ 0.        ,  1.        ,  1.        ],
       [ 0.66666667,  1.        ,  1.        ]])

>>> ColorConv.rgb_to_hsv([(0.5, 0.5, 0.5)])
array([[ 0. ,  0. ,  0.5]])

>>> ColorConv.hsv_to_rgb([(0.1, 0.1, 0.1), (0.5, 0.5, 1)])
array([[ 0.1  ,  0.096,  0.09 ],
       [ 0.5  ,  1.   ,  1.   ]])

>>> ColorConv.hsv_to_rgb(ColorConv.rgb_to_hsv([(0.1, 0.1, 0.1), (0.5, 0.5, 1)]))
array([[ 0.1,  0.1,  0.1],
       [ 0.5,  0.5,  1. ]])
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorConv
