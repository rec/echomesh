from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

import cechomesh

from echomesh.pattern.Maker import maker
from echomesh.pattern.Pattern import Pattern

@maker
def concatenate(light_sets):
  return cechomesh.concatenate_color_lists(light_sets)

class Concatenate(Pattern):
  def _evaluate(self):
    return cechomesh.concatenate_color_lists(
