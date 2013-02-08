"""
>>> [WheelColor.wheel_color(r / 10.0) for r in range(11)]
[array([ 0.,  1.,  0.]), array([ 0.3,  0.7,  0. ]), array([ 0.6,  0.4,  0. ]), array([ 0.9,  0.1,  0. ]), array([ 0. ,  0.2,  0.8]), array([ 0. ,  0.5,  0.5]), array([ 0. ,  0.8,  0.2]), array([ 0.9,  0. ,  0.1]), array([ 0.6,  0. ,  0.4]), array([ 0.3,  0. ,  0.7]), array([ 0.,  1.,  0.])]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.lights import WheelColor
