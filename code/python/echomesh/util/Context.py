from echomesh.base import Name
from echomesh.base import Platform

CONTEXTS = ['tag', 'name', 'platform', 'master', 'default']

def resolve(context):
  parts = context.split('/')
  body = parts[0]
  suffix = parts[1] if len(parts) >= 2 else ''

  if body not in CONTEXTS:
    raise Exception('Didn\'t understand "%s" in context %s.' % (body, context))

  if body == 'name':
    suffix = suffix or ('/' + Name.NAME)

  elif body == 'platform':
    suffix = suffix or ('/' + Platform.PLATFORM)

  elif suffix:
    raise Exception("Name not needed for %s" % body)

  return '%s%s' % (body, suffix)

