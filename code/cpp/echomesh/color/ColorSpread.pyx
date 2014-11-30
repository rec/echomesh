import six

def _even_color_slots(int size, int slots):
    slot = 0
    for i in range(slots):
        previous = slot
        slot = int(math.ceil(((i + 1) * size) / slots))
        yield slot - previous - 1

def _to_list(s, base_type, **kwds):
    if not s:
        return []
    if not isinstance(s, list):
        if isinstance(s, six.string_types):
            s = [i.strip() for i in s.split(', ')]
        elif isinstance(s, tuple):
            s = list(s)
        else:
            s = [s]
    return [i if isinstance(i, base_type) else base_type(i, **kwds) for i in s]

def _ensure_length(list x, int length):
    if len(x) < length:
        x.extend([x[-1]] * length - len(x))
    else:
        while len(x) > length:
            x.pop()

def color_spread(colors, model=None, max_steps=None, steps=None,
                 total_steps=None, transform=None):
    cdef Color c1
    cdef Color c2
    cdef FColor f1
    cdef FColor f2
    cdef const ColorModel* cmodel

    if not colors:
        raise Exception('spread: There must be at least two colors.')

    if steps and total_steps:
        raise ValueError('spread: Can only set one of steps and total_steps')

    cl = ColorList()

    if len(colors) == 1:
        c1 = Color(colors[0])
        single_steps = total_steps or max_steps
        if steps:
            if len(steps) > 1:
                raise Exception(
                  'This spread only has one color %s but more than one step' % c1)
            single_steps = steps[0] or single_steps

        cl.thisptr.resize(single_steps)
        cl.set_all(c1)
        return cl

    if model and model != 'rgb':
        cmodel = get_color_model(model)
    else:
        cmodel = NULL

    cdef ColorList colors2
    colors2 = ColorList(colors)
    transform = _to_list(transform, Transform)
    lc = len(colors2)
    if transform:
        _ensure_length(transform, lc - 1)

    try:
        steps = list(steps)
    except TypeError:
        steps = steps and [steps]

    if steps:
        _ensure_length(steps, lc - 1)
    else:
        steps = list(_even_color_slots((total_steps or max_steps) - 1, lc - 1))

    cl.thisptr.resize(sum(steps) + lc)
    pos = 0
    for i, step in enumerate(steps):
        c1 = colors2[i]
        c2 = colors2[i + 1]
        f1 = c1.thisptr[0]
        f2 = c2.thisptr[0]
        if cmodel:
            f1 = cmodel.fromRgb(f1)
            f2 = cmodel.fromRgb(f2)

        tr = (transform and transform[i].apply) or (lambda x: x)
        for j in range(step + 2):
            inc = tr(j / (step + 1.0))
            if cmodel:
                cl.thisptr.set(pos, cmodel.toRgb(cmodel.interpolate(f1, f2, inc)))
            else:
                cl.thisptr.set(pos, f1.interpolate(f2, inc, 0, 0))
            pos += 1
        pos -= 1

    return cl

def even_color_spread(steps, *colors):
    return color_spread(colors, None, steps, None, None, None)
