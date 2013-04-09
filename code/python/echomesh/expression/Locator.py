from __future__ import absolute_import, division, print_function, unicode_literals

import functools

def get_variable(element, category, parts):
  if category == 'global':
    from echomesh.element import ScoreMaster
    element = ScoreMaster.INSTANCE.get_prefix(parts.pop(0))[1]
  elif category == 'element':
    element = element.get_root()
  elif category == 'parent':
    element = element.parent
  else:
    assert category == 'local', 'Bad category %s' % category

  variable = parts.pop()
  for p in parts:
    element = element.get_child(p)
  return element.variables[variable]
