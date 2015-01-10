from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Join

class PrefixException(KeyError):
    def __init__(self, key, *args, **kwds):
        args = ' '.join(a for a in args if a)
        super(PrefixException, self).__init__(key, args, **kwds)

    def __str__(self):
        return self.args[1]

_NONE = object()

def get_prefix(table, key, allow_prefixes=True, exception_prefix=''):
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
            raise PrefixException(key, exception_prefix,
                                  '"%s" matches more than one:' % key, cmds)
    raise PrefixException(key, exception_prefix, '"%s" is not valid' % key)

def set_assignment(
        address, value, master, slave, unmapped_keys=None, exception_prefix=''):
    unmapped = False
    keys = address.split('.')
    for i, key in enumerate(keys):
        if unmapped:
            new_master = master.get(key, {})
        else:
            key, new_master = get_prefix(master, key,
                                         exception_prefix=exception_prefix)
        if i == len(keys) - 1:
            slave[key] = value
        else:
            master = new_master
            slave = slave.setdefault(key, {})
        if (not i) and unmapped_keys and key in unmapped_keys:
            unmapped = True

class PrefixDict(dict):
    allow_prefixes = True
    name = ''

    def get_prefix(self, key):
        prefix = self.name and ('In table %s,' % self.name)
        return get_prefix(self, key,
                          exception_prefix=prefix,
                          allow_prefixes=self.allow_prefixes)

    def __getitem__(self, key):
        return self.get_prefix(key)[1]

    def __contains__(self, key):
        try:
            self[key]
            return True
        except:
            return False
