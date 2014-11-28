from __future__ import absolute_import, division, print_function, unicode_literals

SETTINGS_EXCEPTIONS = set(['load', 'map', 'new', 'start'])

def _merge_or_diff(old, new, is_merge, require_old_key, path='',
                   require_old_key_exceptions=None):
    """Merges two dictionaries, mutating the dictionary "old"."""
    nothing = ()
    require_old_key_exceptions = require_old_key_exceptions or set()

    if old is None:
        old = {}
        require_old_key = False
    else:
        # old = copy.deepcopy(old)
        pass

    import six
    for key, new_v in six.iteritems(new or {}):
        new_path = '%s:%s' % (path, key)
        old_v = old.get(key, nothing)

        if old_v is nothing:
            if is_merge:
                if require_old_key and (key not in require_old_key_exceptions):
                    raise Exception(
                        'Tried to override non-existent key ' + new_path)
                else:
                    old[key] = new_v
            else:
                continue

        if isinstance(old_v, dict):
            if isinstance(new_v, dict):
                is_exception = key in require_old_key_exceptions
                _merge_or_diff(old_v, new_v, is_merge,
                               require_old_key and not is_exception, new_path)
            else:
                raise Exception(
                    'Tried to override dict with non-dict for key ' + new_path)

        elif not isinstance(new_v, dict):
            if is_merge:
                old[key] = new_v
            else:
                del old[key]

        elif require_old_key:
            raise Exception('Tried to override non-dict with dict for key ' +
                            new_path)

        elif is_merge:
            old[key] = new_v

    return old

def difference_strict(old, new):
    return _merge_or_diff(old, new, False, True)

def difference(old, new):
    return _merge_or_diff(old, new, False, False)

def merge_strict(*others, **kwds):
    def _merge(old, new):
        return _merge_or_diff(old, new, True, True)

    return reduce(_merge, others + (kwds, ), None)

def merge_strict_with_exceptions(exceptions, *others):
    def _merge(old, new):
        return _merge_or_diff(old, new, True, True,
                              require_old_key_exceptions=exceptions)

    return reduce(_merge, others, None)

def merge(*others, **kwds):
    def _merge(old, new):
        return _merge_or_diff(old, new, True, False)

    return reduce(_merge, others + (kwds, ), None)

def merge_for_settings(*settings):
    return merge_strict_with_exceptions(SETTINGS_EXCEPTIONS, *settings)
