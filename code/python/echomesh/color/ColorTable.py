import cechomesh

def to_color(color):
  if isinstance(color, (tuple, list)):
    return color
  if isinstance(color, int):
    return cechomesh.int_to_color(color)

  c = cechomesh.string_to_color(color)
  if c:
    return c
  raise Exception("Didn't understand color name %s." % color)
