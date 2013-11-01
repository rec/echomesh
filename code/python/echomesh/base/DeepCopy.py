from __future__ import absolute_import, division, print_function, unicode_literals

def deepcopy(x):
  if isinstance(x, dict):
    return dict((k, deepcopy(v)) for k, v in x.items())

  if isinstance(x, list):
    return [deepcopy(i) for i in x]

  if isinstance(x, tuple):
    return tuple(deepcopy(i) for i in x)

  return x
