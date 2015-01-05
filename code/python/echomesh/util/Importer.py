from __future__ import absolute_import, division, print_function, unicode_literals

import importlib

def importer(classpath):
    try:
        # Try to import a module.
        return importlib.import_module(classpath)
    except ImportError:
        # Try to import a function out of a module.
        parts = classpath.split('.')
        function = classpath.pop()
        return getattr(importlib.import_module(classpath), function)
