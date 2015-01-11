from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base.GetPrefix import PrefixDict
from echomesh.util.Importer import importer
from echomesh.util.string.Formatted import Formatted

class Command(Formatted):
    FORMAT_MEMBERS = 'name', 'help'
    DEFER_LOADING = True

    def __init__(self, classpath, name, importer=importer):
        self.classpath = classpath
        self.name = name
        self.importer = importer
        self._loaded = not Command.DEFER_LOADING
        self._load()

    def _load(self):
        if not self._loaded:
            mod = self.importer('%s.%s' % (self.classpath, self.name))
            get = lambda key: getattr(mod, key, None)

            self.call = get('COMMAND') or get(self.name.lower())
            assert (self.call)
            self._help = get('HELP')
            self._loaded = True

    def __call__(self, *args, **kwds):
        self._load()
        return self.call(*args, **kwds)

    def help(self):
        self._load()
        return self._help


class Registry(PrefixDict):
    def __init__(self, name, base_path, more_paths,
                 allow_prefixes=True, importer=importer):
        super(Registry, self).__init__()
        self.allow_prefixes = allow_prefixes
        self.name = name
        if isinstance(more_paths, six.string_types):
            classpaths = (c.strip() for c in more_paths.split(':'))
            classpaths = [c for c in classpaths if c]
        else:
            classpaths = list(more_paths)
        classpaths.append(base_path)

        self.help_table = PrefixDict(name=name, allow_prefixes=allow_prefixes)
        for cp in reversed(classpaths):
            module = importer(cp)
            for name in getattr(module, '__all__'):
                command = Command(cp, name)
                self[name.lower()] = command
            self.help_table.update(getattr(module, 'HELP', {}))

    def help(self, key):
        return self.help_table.get(key) or self[key].help()
