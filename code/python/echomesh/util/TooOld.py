from echomesh.base import Version

def too_old():
  if Version.TOO_OLD:
    print Version.ERROR
