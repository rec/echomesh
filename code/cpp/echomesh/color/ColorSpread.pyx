import six

def _even_color_slots(int size, int slots):
  slot = 0
  for i in range(slots):
    previous = slot
    slot = int(math.ceil(((i + 1) * size) / slots))
    yield slot - previous - 1

def _to_list(s, base_type):
  if not s:
    return []
  if not isinstance(s, list):
    if isinstance(s, six.string_types):
      s = [i.strip() for i in s.split(', ')]
    elif isinstance(s, tuple):
      s = list(s)
    else:
      s = [s]
  return [i if isinstance(i, base_type) else base_type(i) for i in s]

def _ensure_length(list x, int length):
  if len(x) < length:
    x.extend([x[-1]] * length - len(x))
  else:
    while len(x) > length:
      x.pop()

def color_spread(colors, model, max_steps=None, steps=None, total_steps=None, transform=None):
  # TODO: hsv!
  cdef Color c1
  cdef Color c2

  if not colors or len(colors) <= 1:
    raise Exception('spread: There must be at least two colors.')

  if not (steps is None or total_steps is None):
    raise ValueError('spread: Can only set one of steps and total_steps')

  colors = _to_list(colors, Color)
  transform = _to_list(transform, Transform)
  lc = len(colors)
  if transform:
    _ensure_length(transform, lc - 1)
  if steps:
    _ensure_length(steps, lc - 1)
  else:
    steps = _even_color_slots((total_steps or max_steps) - 1, lc - 1)

  steps = list(steps)
  cl = ColorList(model=model)
  cl.thisptr.resize(sum(steps) + lc)
  pos = 0
  for i, step in enumerate(steps):
    c1 = colors[i]
    c2 = colors[i+1]
    tr = (transform and transform[i].apply) or (lambda x: x)
    for j in range(step + 2):
      inc = j / (step + 1.0)
      cl.thisptr.set(c1.thisptr.interpolate(c2.thisptr[0], tr(inc)), pos)
      pos += 1
    pos -= 1

  return cl

def even_color_spread(steps, *colors):
  return color_spread(colors, None, steps, None, None, None)
