from __future__ import absolute_import, division, print_function, unicode_literals

INFINITY = float('inf')

# Includes begin and end!
def interval(count=None, begin=None, end=None, skip=None):
  assert count is None or count >= 0
  missing = (begin is None or end is None)
  assert missing or count is None or skip is None
  if skip is None:
    if missing:
      skip = 1
    elif count is None:
      skip = 1 if begin <= end else -1
    else:
      skip = (end - begin) // (count + 1)
  else:
    assert skip != 0
    if not missing:
      assert skip > 0 or begin >= end
      assert skip < 0 or begin <= end

  if begin is None:
    if end is not None and count is not None:
      begin = end - (count - 1) * skip
    else:
      begin = 0

  if end is None:
    if begin is not None and count is not None:
      end = begin + (count - 1) * skip
    else:
      end = INFINITY

  if count is None:
    if end == INFINITY:
      count = INFINITY
    else:
      count = 1 + (end - begin) // skip

  return count, begin, end, skip
