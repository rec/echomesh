from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Join

class PrefixException(Exception):
  pass

_NONE = object()

def get_prefix(table, name, allow_prefixes=True):
  """
  Looks up an entry in a table where unique prefixes are allowed.
  """
  result = table.get(name, _NONE)
  if result is not _NONE:
    return name, result

  if allow_prefixes:
    results = [(k, v) for (k, v) in table.iteritems() if k.startswith(name)]
    if len(results) == 1:
      return results[0]
    elif len(results) > 1:
      words = sorted(x[0] for x in results)
      cmds = Join.join_words(words)
      raise PrefixException('"%s" matches more than one: %s.' % (name, cmds))
  raise PrefixException('"%s" is not valid.' % (name))
