"""
>>> list(split_args([]))
[]

>>> list(split_args(['extra=32']))
[([u'extra'], u'32')]

>>> list(split_args(['extra=', '32']))
[([u'extra'], u'32')]

>>> list(split_args(['extra', '=32']))
[([u'extra'], u'32')]

>>> list(split_args(['extra', '=', '32']))
[([u'extra'], u'32')]

>>> list(split_args(['ac:', ':de:', '=', ':defeg:']))
[([u'ac', u'de'], u':defeg:')]

>>> list(split_args(['extra=', '32 men', 'ac:', ':de:', '=', ':defeg:']))
[([u'extra'], u'32 men'), ([u'ac', u'de'], u':defeg:')]


>>> split_args_to_dict([])
{}

>>> split_args_to_dict(['extra=32'])
{u'extra': u'32'}

>>> split_args_to_dict(['extra=', '32'])
{u'extra': u'32'}

>>> split_args_to_dict(['extra', '=32'])
{u'extra': u'32'}

>>> split_args_to_dict(['extra', '=', '32'])
{u'extra': u'32'}

>>> split_args_to_dict(['ac:', ':de:', '=', ':defeg:'])
{u'ac': {u'de': u':defeg:'}}

>>> sorted(split_args_to_dict(['extra=', '32 men', 'ac:', ':de:', '=', ':defeg:']).iteritems())
[(u'ac', {u'de': u':defeg:'}), (u'extra', u'32 men')]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base.Args import *
