from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Join

class PrefixException(Exception):
    pass

_NONE = object()

def get_prefix(table, name, allow_prefixes=True):
    """
    Looks up an entry in a table where unique prefixes are allowed.
    """
    result = table.get(name, _NONE)
    if result is not _NONE:
        return name, result

    if allow_prefixes:
        results = [(k, v) for (k, v) in six.iteritems(table)
                   if k.startswith(name)]
        if len(results) == 1:
            return results[0]
        elif len(results) > 1:
            words = sorted(x[0] for x in results)
            cmds = Join.join_words(words)
            raise PrefixException('"%s" matches more than one: %s' %
                                  (name, cmds))
    raise PrefixException('"%s" is not valid' % (name))

def get(table, name, allow_prefixes=True):
    try:
        return get_prefix(table, name, allow_prefixes)
    except PrefixException:
        return None

def set_assignment(address, value, master, slave, unmapped_names=None):
    unmapped = False
    names = address.split('.')
    for i, name in enumerate(names):
        if unmapped:
            new_master = master.get(name, {})
        else:
            name, new_master = get_prefix(master, name)
        if i == len(names) - 1:
            slave[name] = value
        else:
            master = new_master
            slave = slave.setdefault(name, {})
        if (not i) and unmapped_names and name in unmapped_names:
            unmapped = True
