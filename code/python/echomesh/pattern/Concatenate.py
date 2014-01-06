from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

import cechomesh

from echomesh.pattern.Maker import maker

@maker
def concatenate(light_sets):
  return list(itertools.chain(*light_sets))
