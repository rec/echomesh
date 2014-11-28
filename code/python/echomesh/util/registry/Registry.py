from __future__ import absolute_import, division, print_function, unicode_literals

from collections import namedtuple

import sys

from echomesh.base.AddExceptionSuffix import add_exception_suffix
from echomesh.base import GetPrefix
from echomesh.base import Join
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Registry(object):
    def __init__(self, name, case_insensitive=True, allow_prefixes=True,
                 class_path=None):
        self._registry = {}
        self.name = name
        self.case_insensitive = case_insensitive
        self.allow_prefixes = allow_prefixes
        self.class_path = class_path

    def register(self, function, function_name=None,
                 help_text=None, see_also=None):
        function_name = function_name or function.__name__
        if self.case_insensitive:
            function_name = function_name.lower()

        entry = self._registry.get(function_name, None)
        if not entry:
            from echomesh.util.registry import Entry
            self._registry[function_name] = Entry.Entry(
              function_name, function, help_text, see_also, self)
        else:
            if entry.function is not function:
                raise Exception(
                    'Conflicting registrations for %s' % function_name)
            else:
                LOGGER.error(
                    'Duplicate entry for %s in registry %s', function_name,
                             self.name)

    def register_all(self, **kwds):
        for item_name, item in kwds.items():
            help_text, see_also = None, None
            if isinstance(item, (list, tuple)):
                if len(item) > 1:
                    help_text = item[1]
                    if len(item) > 2:
                        see_also = item[2]
                item = item[0]
            self.register(item, item_name, help_text, see_also)

    def entry(self, name):
        try:
            entry = GetPrefix.get_prefix(
              self._registry, name, allow_prefixes=self.allow_prefixes)[1]
            entry.resolve_function()
            return entry
        except:
            add_exception_suffix(' in registry "%s"' % self.name)

    def get(self, name):
        return self.function(name)

    def function(self, name):
        return self.entry(name).function

    def get_help(self, name):
        return self.entry(name).help()

    def get_from_description(self, description, default_type=None):
        """Pops a type out of a description and uses it to locate a registry
           item.
        """
        type_value = description.pop('type', default_type)
        if not type_value:
            raise Exception('No %s type found' % self.name)
        try:
            return self.entry(type_value)
        except GetPrefix.PrefixException:
            raise Exception('Didn\'t understand %s type="%s"' %
                            (self.name, type_value))

    def make_from_description(self, description, default_type=None):
        entry = self.get_from_description(description, default_type)
        if entry.function:
            return entry.function(**description)
        else:
            raise Exception("Didn't understand description %s" % description)

    def join_keys(self, command_only=True, load=True):
        words = []
        for key, entry in self._registry.items():
            load and entry.resolve_function()
            if (not command_only) or entry.function:
                words.append(key)
        return Join.join_words(words)

    def keys(self):
        return self._registry.keys()

    def dump(self, printer=print, load=True):
        for k, v in self._registry.items():
            load and v.resolve_function()
            printer(k, v)
