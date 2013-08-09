from __future__ import absolute_import, division, print_function, unicode_literals

from collections import namedtuple

import six
import sys

from echomesh.base import GetPrefix
from echomesh.base import Join
from echomesh.util import Importer
from echomesh.util import Log
from echomesh.util.registry.Entry import Entry

LOGGER = Log.logger(__name__)

class Registry(object):
  def __init__(self, name, case_insensitive=True, allow_prefixes=True,
               class_path=None):
    self.registry = {}
    self.name = name
    self.case_insensitive = case_insensitive
    self.allow_prefixes = allow_prefixes
    self.class_path = class_path

  def register(self, function, function_name=None,
               help_text=None, see_also=None):
    function_name = function_name or function.__name__
    if self.case_insensitive:
      function_name = function_name.lower()

    entry = self.registry.get(function_name, None)
    if not entry:
      self.registry[function_name] = Entry(
        function_name, function, help_text, see_also, self)
    else:
      if entry.function is not function:
        raise Exception('Conflicting registrations for %s' % function_name)
      else:
        LOGGER.error('Duplicate entry for %s in registry %s', function_name,
                     self.name)

  def register_all(self, **kwds):
    for item_name, item in six.iteritems(kwds):
      help_text, see_also = None, None
      if isinstance(item, (list, tuple)):
        if len(item) > 1:
          help_text = item[1]
          if len(item) > 2:
            see_also = item[2]
        item = item[0]
      self.register(item, item_name, help_text, see_also)

  def entry(self, name):
    return GetPrefix.get_prefix(self.registry, name,
                                allow_prefixes=self.allow_prefixes)[1]

  def get(self, name):
    return self.function(name)

  def function(self, name):
    return self.entry(name).load().function

  def help(self, name):
    return self.entry(name).load().help()

  def keys(self):
    return self.registry.keys()

  def join_keys(self, command_only=True):
    # TODO: not loading for this, will this work?
    w = (k for (k, entry) in six.iteritems(self.registry)
         if (not command_only) or entry.function)
    return Join.join_words(w)

  def dump(self, printer=print, load=True):
    for k, v in six.iteritems(self.registry):
      load and v.load()
      printer(k, v)
