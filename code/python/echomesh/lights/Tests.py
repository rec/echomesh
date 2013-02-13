"""
>>> [WheelColor.wheel_color(r / 10.0) for r in range(11)]
[array([ 0.,  1.,  0.]), array([ 0.3,  0.7,  0. ]), array([ 0.6,  0.4,  0. ]), array([ 0.9,  0.1,  0. ]), array([ 0. ,  0.2,  0.8]), array([ 0. ,  0.5,  0.5]), array([ 0. ,  0.8,  0.2]), array([ 0.9,  0. ,  0.1]), array([ 0.6,  0. ,  0.4]), array([ 0.3,  0. ,  0.7]), array([ 0.,  1.,  0.])]

>>> ColorConv.rgb_to_hsv([0, 0, 0])
array([[ 0.,  0.,  0.]], dtype=float32)

>>> ColorConv.rgb_to_hsv([[0, 0, 0]])
array([[ 0.,  0.,  0.]], dtype=float32)

>>> ColorConv.rgb_to_hsv([(1, 1, 1)])
array([[ 0.,  0.,  1.]], dtype=float32)

>>> ColorConv.rgb_to_hsv([[1.0, 0, 0], [0, 0, 1.0]])
array([[ 0.        ,  1.        ,  1.        ],
       [ 0.66666669,  1.        ,  1.        ]], dtype=float32)

>>> ColorConv.rgb_to_hsv([(0.5, 0.5, 0.5)])
array([[ 0. ,  0. ,  0.5]], dtype=float32)

>>> ColorConv.hsv_to_rgb([(0.1, 0.1, 0.1), (0.5, 0.5, 1)])
array([[[ 0.1  ,  0.096,  0.09 ],
        [ 0.5  ,  1.   ,  1.   ]]], dtype=float32)

>>> ColorConv.hsv_to_rgb(ColorConv.rgb_to_hsv([(0.1, 0.1, 0.1), (0.5, 0.5, 1)]))
array([[[ 0.1,  0.1,  0.1],
        [ 0.5,  0.5,  1. ]]], dtype=float32)

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.lights import ColorConv
from echomesh.lights import WheelColor
