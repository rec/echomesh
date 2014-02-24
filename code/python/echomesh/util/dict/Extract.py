from __future__ import absolute_import, division, print_function, unicode_literals

def extract(description, *names):
  result = {}
  for field in names:
    if field in description:
      result[field] = description.pop(field)
  return result
