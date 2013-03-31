"""
>>> ColorTable.to_color('black')
(0.0, 0.0, 0.0)

>>> ColorTable.to_color('white')
(1.0, 1.0, 1.0)

>>> ColorTable.to_color('pink')
(1.0, 0.7529411764705882, 0.796078431372549)

>>> ColorTable.to_color('gray')
(0.5019607843137255, 0.5019607843137255, 0.5019607843137255)

>>> ColorTable.to_color('grey')
(0.5019607843137255, 0.5019607843137255, 0.5019607843137255)

>>> ColorTable.to_color('grey 3')
(0.03137254901960784, 0.03137254901960784, 0.03137254901960784)

>>>
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorTable
