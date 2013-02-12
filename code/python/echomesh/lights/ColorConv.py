from __future__ import absolute_import, division, print_function, unicode_literals

# Code adapted from the skimage project.

from echomesh.util import Importer
numpy = Importer.imp('numpy')

def _prepare_colorarray(arr):
  if isinstance(arr, numpy.ndarray):
    return arr

  if not arr:
    return numpy.array([])

  try:
    arr[0][0]
  except TypeError:
    arr = [arr]

  return numpy.array(arr)


def rgb_to_hsv(rgb):
  """RGB to HSV color space conversion."""
  arr = _prepare_colorarray(rgb)
  out = numpy.empty_like(arr)

  # -- V channel
  out_v = arr.max(-1)

  # -- S channel
  delta = arr.ptp(-1)

  # Ignore warning for zero divided by zero
  old_settings = numpy.seterr(divide='ignore', invalid='ignore')
  try:
    out_s = delta / out_v
    out_s[delta == 0.] = 0.

    # -- H channel
    # Red is max.
    idx = (arr[:, 0] == out_v)
    out[idx, 0] = (arr[idx, 1] - arr[idx, 2]) / delta[idx]

    # Green is max
    idx = (arr[:, 1] == out_v)
    out[idx, 0] = 2. + (arr[idx, 2] - arr[idx, 0]) / delta[idx]

    # Blue is max.
    idx = (arr[:, 2] == out_v)
    out[idx, 0] = 4. + (arr[idx, 0] - arr[idx, 1]) / delta[idx]
    out_h = (out[:, 0] / 6.) % 1.
    out_h[delta == 0.] = 0.
  finally:
    numpy.seterr(**old_settings)

  # -- Output
  out[:, 0] = out_h
  out[:, 1] = out_s
  out[:, 2] = out_v

  # Remove NaNs
  out[numpy.isnan(out)] = 0
  return out


def hsv_to_rgb(hsv):
  """HSV to RGB color space conversion."""
  arr = _prepare_colorarray(hsv)

  hi = numpy.floor(arr[:, 0] * 6)
  f = arr[:, 0] * 6 - hi
  p = arr[:, 2] * (1 - arr[:, 1])
  q = arr[:, 2] * (1 - f * arr[:, 1])
  t = arr[:, 2] * (1 - (1 - f) * arr[:, 1])
  v = arr[:, 2]

  hi = numpy.dstack([hi, hi, hi]).astype(numpy.uint8) % 6
  out = numpy.choose(hi, [numpy.dstack((v, t, p)),
                          numpy.dstack((q, v, p)),
                          numpy.dstack((p, v, t)),
                          numpy.dstack((p, q, v)),
                          numpy.dstack((t, p, v)),
                          numpy.dstack((v, p, q))])

  return out

