import re

from echomesh.base import Name
from echomesh.base import Platform

SCOPES = ['tag', 'name', 'platform', 'master', 'default']

def resolve(scope):
  parts = scope.split('/')
  body = parts[0]
  suffix = parts[1] if len(parts) >= 2 else ''

  if body not in SCOPES:
    raise Exception("Didn't understand body %s in scope %s." % (body, scope))

  if body == 'name':
    suffix = suffix or ('/' + Name.NAME)

  elif body == 'platform':
    suffix = suffix or ('/' + Platform.PLATFORM)

  elif suffix:
    raise Exception("Name not needed for %s" % body)

  return '%s%s' % (body, suffix)

