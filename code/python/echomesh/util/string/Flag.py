from __future__ import absolute_import, division, print_function, unicode_literals

def split_flag(flag):
    parts = flag.lstrip('-').split('=', 1)
    flag = parts.pop(0)
    return flag, ((parts and parts[0]) or True)

def split_flag_args(args):
    flags, new_args = {}, []

    for a in args:
        if a.startswith('-'):
            name, value = split_flag(a)
            if name in flags:
                raise Exception('Repeated flag %s' % name)
            flags[name] = value
        else:
            new_args.append(a)

    return flags, new_args
