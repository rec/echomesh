from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import yaml

from echomesh.base.AddExceptionSuffix import add_exception_suffix
from echomesh.base.DataFileName import data_filename

from contextlib import closing

SEPARATOR_BASE = '---'
SEPARATOR = '\n%s\n' % SEPARATOR_BASE
PROPAGATE_EXCEPTIONS = False

def encode_one(item, **kwds):
    return yaml.safe_dump(item, **kwds)

def decode(s):
    return list(yaml.safe_load_all(s))

def decode_one(s):
    return yaml.safe_load(s)

def read(fname, file_type='', allow_empty=True):
    def error(state, e):
        if file_type:
            msg = 'in %s %s file %s.' % (state, file_type, fname)
        else:
            msg = 'in %s file %s.' % (state, fname)
        add_exception_suffix(msg)
        raise

    try:
        f = _open_userfile(fname, 'r')
    except Exception as e:
        if not allow_empty:
            error('reading', e)
        return []

    with closing(f):
        try:
            return decode(f)
        except Exception as e:
            error('decoding', e)

def write(fname, *items):
    try:
        written = False
        with closing(_open_userfile(fname, 'w')) as f:
            if written:
                f.write(SEPARATOR)
            yaml.safe_dump_all(items, f)
    except Exception as e:
        print("Can't write filename", fname, e.message)
        if PROPAGATE_EXCEPTIONS:
            raise

def _open_userfile(fname, perms='r'):
    return open(data_filename(os.path.expanduser(fname)), perms)
