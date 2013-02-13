"""
>>> [WheelColor.wheel_color(r / 10.0) for r in range(11)]
[array([ 0.,  1.,  0.]), array([ 0.3,  0.7,  0. ]), array([ 0.6,  0.4,  0. ]), array([ 0.9,  0.1,  0. ]), array([ 0. ,  0.2,  0.8]), array([ 0. ,  0.5,  0.5]), array([ 0. ,  0.8,  0.2]), array([ 0.9,  0. ,  0.1]), array([ 0.6,  0. ,  0.4]), array([ 0.3,  0. ,  0.7]), array([ 0.,  1.,  0.])]

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
array([[[ 0.1  ,  0.096,  0.09 ],
        [ 0.5  ,  1.   ,  1.   ]]])

>>> ColorConv.hsv_to_rgb(ColorConv.rgb_to_hsv([(0.1, 0.1, 0.1), (0.5, 0.5, 1)]))
array([[[ 0.1,  0.1,  0.1],
        [ 0.5,  0.5,  1. ]]])

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

from echomesh.color import ColorConv, ColorSpread, WheelColor
