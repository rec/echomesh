from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

def has_extension(f):
    return f.endswith('.yml') or f.endswith('.json')

def data_filename(name):
    if os.path.exists(name):
        return name
    if not has_extension(name):
        n = name + '.yml'
        if os.path.exists(n):
            return n
        n = name + '.json'
        if os.path.exists(n):
            return n
    raise Exception("Couldn't find a file matching %s" % name)
