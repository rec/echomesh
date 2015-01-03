from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os
from collections import namedtuple

from echomesh.base import Args
from echomesh.base import DataFile
from echomesh.base import GetPrefix
from echomesh.base import Leafs
from echomesh.base import Merge
from echomesh.base import Yaml

_ARGUMENT_ERROR = """
ERROR: Didn't understand arguments to echomesh: "%s".

echomesh needs to be called with arguments looking like "name=value".

Examples:
  echomesh
  echomesh debug=true
  echomesh audio.input.enable=false light.enable=false
"""

_ASSIGNMENT_ERROR = """
ERROR: couldn't assign a variable from: "%s".

Variable assignments look like "name=value" and you can have more than one
per line.

Examples:
  debug=true
  audio.input.enable=false light.enable=false
"""

FileSettings = namedtuple('FileSettings', 'file base edits changes')

class MergeSettings(object):
    def __init__(self, settings):
        self.settings = settings
        self._read()

    def _read(self):
        self._read_file_settings()
        self.arg_settings = self._assignment_to_settings(
            self.settings, _ARGUMENT_ERROR)
        return self.recalculate()

    def recalculate(self):
        self.settings = None
        self.changed = {}
        for _, settings in self.file_settings:
            self.settings = Merge.merge(self.settings, *settings)
            self.changed = Merge.merge(self.changed, *settings[2:])

        arg = copy.deepcopy(self.arg_settings)
        clean_arg = Merge.difference_strict(arg, self.changed)
        self.settings = Merge.merge_for_settings(self.settings, clean_arg)

        return self.settings

    def has_changes(self):
        return any(settings[2] for (_, settings) in self.file_settings)

    def get_changes(self):
        return [(f, c[2]) for (f, c) in self.file_settings if c[2]]

    def assign(self, args, index=2):  # default is 'master'
        settings = self.file_settings[index][1]

        while len(settings) < 3:
            settings.append({})
        assignments = self._assignment_to_settings(args, _ASSIGNMENT_ERROR)
        settings[2] = Merge.merge(settings[2], assignments)
        self.recalculate()
        return assignments

    def save(self):
        saved_files = []
        for f, settings in self.file_settings:
            if len(settings) > 2 and settings[2]:
                saved_files.append(f)
                settings[1] = Merge.merge(*settings[1:])
                while len(settings) > 2:
                    settings.pop()
                if os.path.exists(f):
                    with open(f, 'r') as fo:
                        data = fo.read().split(Yaml.SEPARATOR)[0]
                else:
                    data = ''

                parent = os.path.dirname(f)
                if not os.path.exists(parent):
                    print('Creating directory', parent)
                    os.makedirs(parent)

                with open(f, 'wb') as fw:
                    if data:
                        fw.write(data)
                        fw.write(Yaml.SEPARATOR)
                    fw.write(Yaml.encode_one(settings[1]))

        self.arg_settings = Merge.difference_strict(
            self.arg_settings, self.changed)
        self.recalculate()
        return saved_files

    def assignments(self, index=2):
        assigned = self.file_settings[index][1]
        return (len(assigned) > 2 and Leafs.leafs(assigned[2])) or {}

    def _read_file_settings(self):
        self.file_settings = []
        base_settings = None

        for f in reversed(DataFile.expand_settings()):
            settings = Yaml.read(f, 'settings')
            for c in settings:
                if base_settings:
                    base_settings = Merge.merge_for_settings(base_settings, c)
                else:
                    base_settings = copy.deepcopy(c)
            while len(settings) < 3:
                settings.append({})
            self.file_settings.append([f, settings])

    def _assignment_to_settings(self, args, error):
        args = ' '.join(args)
        settings = {}
        base_settings = self.file_settings[0][1][0]
        assert isinstance(base_settings, dict)
        try:
            split_args = Args.split(args)
        except Exception as e:
            e.arg = '%s %s' % (error, args)
            raise

        for addr, value in split_args:
            try:
                GetPrefix.set_assignment(
                    addr, value, base_settings, settings,
                    unmapped_names=Merge.SETTINGS_EXCEPTIONS)
            except GetPrefix.PrefixException:
                raise Exception('Can\'t understand settings address "%s"' %
                                addr)
            except Exception:
                raise Exception(
                    'Can\'t understand settings value "%s" in %s=%s' %
                    (value, addr, value))
        return settings
