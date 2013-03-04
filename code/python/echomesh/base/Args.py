from __future__ import absolute_import, division, print_function, unicode_literals

def split_args(args):
  address = []
  value = None
  equals_found = False
  for arg in args:
    if equals_found:
      yield address, arg
      address = []
      equals_found = False
      continue
    if '=' in arg:
      name, value = arg.split('=', 1)
      equals_found = True
    else:
      name, value = arg, None

    name = name.strip().strip(':')
    if name:
      address.append(name)

    if value:
      yield address, value
      address = []

  if address:
    print('ERROR: Extra arguments at the end: "%s".' % ' '.join(address))

def split_args_to_dict(args):
  result = {}
  for address, value in split_args(args):
    last = address.pop()
    res = result
    for a in address:
      res = res.setdefault(a, {})
    res[last] = value
  return result
