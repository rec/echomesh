"""
>>> ColorTable.to_color('black')
(0, 0, 0)

>>> ColorTable.to_color('white')
(255, 255, 255)

>>> ColorTable.to_color('pink')
(255, 192, 203)

>>> ColorTable.to_color('gray')
(128, 128, 128)

>>> ColorTable.to_color('grey')
(128, 128, 128)

>>> ColorTable.to_color('grey 3')
(8, 8, 8)

>>>
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorTable
