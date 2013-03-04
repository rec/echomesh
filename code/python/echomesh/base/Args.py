from __future__ import absolute_import, division, print_function, unicode_literals

ARGUMENTS = []  # TODO: perhaps delete?
ASSIGNMENT_ARGS = []
YAML_ARGS = []

def set_arguments(argv):
  ARGUMENTS[:] = args = argv[1:]
  if args:
    a = args[0].strip()
    if _is_yaml(a):
      YAML_ARGS[:] = args
    else:
      ASSIGNMENT_ARGS[:] = split_args(args)

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
