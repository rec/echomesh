from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Join

class PrefixException(Exception):
    pass

_NONE = object()

def get_prefix(table, key, allow_prefixes=True):
    """
    Looks up an entry in a table where unique prefixes are allowed.
    """
    result = table.get(key, _NONE)
    if result is not _NONE:
        return key, result

    if allow_prefixes:
        results = [(k, v) for (k, v) in six.iteritems(table)
                   if k.startswith(key)]
        if len(results) == 1:
            return results[0]
        elif len(results) > 1:
            words = sorted(x[0] for x in results)
            cmds = Join.join_words(words)
            raise PrefixException('"%s" matches more than one: %s' %
                                  (key, cmds))
    raise PrefixException('"%s" is not valid' % (key))

def set_assignment(address, value, master, slave, unmapped_keys=None):
    unmapped = False
    keys = address.split('.')
    for i, key in enumerate(keys):
        if unmapped:
            new_master = master.get(key, {})
        else:
            key, new_master = get_prefix(master, key)
        if i == len(keys) - 1:
            slave[key] = value
        else:
            master = new_master
            slave = slave.setdefault(key, {})
        if (not i) and unmapped_keys and key in unmapped_keys:
            unmapped = True
