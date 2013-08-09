from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Join

_NOT_ACCESSED_ERROR = """\
In an element of type "%s" loaded from "%s", \
the following properties were ignored because they were not understood:

  %s"""

_NOT_ACCESSED_ERROR_SINGLE = """\
In an element of type "%s" loaded from "%s", \
the following property was ignored because it was not understood:

  %s"""

def not_accessed(logger, element, not_accessed_items, element_type):
  if not_accessed_items:
    score = element.get_root().get_property('score') or ''
    if len(not_accessed_items) == 1:
      err = _NOT_ACCESSED_ERROR_SINGLE
    else:
      err = _NOT_ACCESSED_ERROR
    logger.error(err, element_type, score, Join.join_words(not_accessed_items))

