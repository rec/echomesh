# -*- coding: utf-8 -*-
"""
>>> Expression.convert(12)
12

>>> Expression.convert('12')
12

>>> Expression.convert('12 db')
3.9810717055349722

>>> Expression.convert('12dB')
3.9810717055349722

>>> Expression.convert('10 semitones')
1.7817974362806785

>>> Expression.convert('-1 semitone')
0.9438743126816935

>>> Expression.convert('50 cents')
1.029302236643492

>>> Expression.convert('50 cent')
1.029302236643492

>>> Expression.convert('-1.034E+2 semitones')
0.0025475626362608667

>>> Expression.convert('-103.4 semitones')
0.0025475626362608667

>>> Expression.convert('10ms')
0.01

>>> Convert.convert_time('0')

>>> Convert.convert_time('0:0')

>>> Convert.convert_time('0:00')
0

>>> Convert.convert_time('0:01')
1

>>> Convert.convert_time('0:01:00')
60

>>> Convert.convert_time('0:01:00.12')
60.12

>>> Convert.convert_time('1:01:00.12')
3660.12

>>> Expression.convert('13 + 12 ms')
0.025

>>> Expression.convert('1/2sec')
0.5

>>> Expression.convert('(1/2)sec')
0.5

>>> Expression.convert('½sec')
0.5

>>> Expression.convert('1Hz')
1.0

>>> Expression.convert('10 hertz')
0.1

>>> Expression.convert('10 kilohertz')
0.0001

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import Convert
from echomesh.expression import Expression
