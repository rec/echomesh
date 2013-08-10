"""
>>> config = {'hello': 'world', 'deep': {'tree': {'nesting': 'egg'}}}

>>> Setter.setter(config, 'hello')

"""

from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.util.dict import Setter
