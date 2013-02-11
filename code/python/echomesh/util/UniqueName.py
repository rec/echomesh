from __future__ import absolute_import, division, print_function, unicode_literals

import re

MATCH_NAME = re.compile(r'(.*)\.(\d+)$')

def unique_name_match(name, matcher):
  while matcher(name):
    match = MATCH_NAME.match(name)
    if match:
      base, suffix = match.groups()
      suffix = 1 + int(suffix)
    else:
      base, suffix = name, 1
    name = '%s.%d' % (base, suffix)

  return name

def unique_name(name, elements):
  return unique_name_match(name, elements.__contains__)

def unique_file_name(fname, suffix):
  def matcher(name):
    return os.path.exists('%s.%s' % (name, suffix))
  return '%s.%s' % (unique_name_match(fname, matcher), suffix)
