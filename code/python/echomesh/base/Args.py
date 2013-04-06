from __future__ import absolute_import, division, print_function, unicode_literals

ASSIGNMENT_ARGS = []

def set_arguments(argv):
  args = argv[1:]
  if args:
    a = args[0].strip()
    if a:
      ASSIGNMENT_ARGS[:] = split_args(args)

def split_args(args):
  address = []
  value = None
  equals_found = False

  for arg in args:
    if equals_found:
      value = arg
    else:
      if '=' in arg:
        name, value = arg.split('=', 1)
        equals_found = True
      else:
        name, value = arg, None

      address_part = name.strip().strip('.')
      if address_part:
        address.append(name)

    if value:
      clean_address = filter(None, '.'.join(address).split('.'))
      yield clean_address, value
      address = []
      equals_found = False

  if address:
    print('ERROR: Extra arguments at the end: "%s".' % ' '.join(address))

