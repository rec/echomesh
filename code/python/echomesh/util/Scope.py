import re

from echomesh.base import Name
from echomesh.base import Platform

_SCOPE_RE = re.compile(r'( (?: [01234]\. )? ) (\w+) ( (?: / \w+ )? ) $', re.X)

SCOPES = ['local', 'tag', 'name', 'platform', 'global', 'default']

def resolve(scope):
  match = _SCOPE_RE.match(scope)
  if not scope:
    raise Exception("Didn't match: '%s'" % scope)

  prefix, body, suffix = match.groups()
  if body not in SCOPES:
    raise Exception("Didn't understand body %s" % body)

  new_prefix = '%d.' % SCOPES.index(body)
  if prefix and prefix != new_prefix:
    raise Exception("Wrong prefix %s" % body)

  if body == 'name':
    suffix = suffix or ('/' + Name.NAME)

  elif body == 'platform':
    suffix = suffix or ('/' + Platform.PLATFORM)

  elif suffix:
    raise Exception("Name not needed for %s" % body)

  return '%s%s%s' % (new_prefix, body, suffix)

