from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import shutil
import six

from echomesh.remote import RemoteRegistry

from echomesh.base import Settings
from echomesh.base import MakeDirs
from echomesh.base import Path

def transfer(_, **data):
    backup_directory = os.path.join(Path.data_path(), '.echomesh-xfer')

    try:
        shutil.rmtree(backup_directory)
    except OSError:
        pass

    directories = data.get('directories', [])
    if '' in directories:
        directories = os.listdir(Path.data_path())

    for directory in directories:
        parent = os.path.dirname(os.path.join(backup_directory, directory))
        MakeDirs.parent_makedirs(parent)
        shutil.move(os.path.join(Path.data_path(), directory), parent)

    for f, value in six.iteritems(data.get('files')):
        fname = os.path.join(Path.data_path(), f)
        MakeDirs.parent_makedirs(fname)
        with open(fname, 'w') as o:
            o.write(value['contents'])
        os.utime(fname, (value['atime'], value['mtime']))

    if Settings.get('delete_backups_after_transfer'):
        try:
            shutil.rmtree(backup_directory)
        except:
            pass

HELP = """transfer:  transfer all your files to all the other echomesh nodes.
"""
