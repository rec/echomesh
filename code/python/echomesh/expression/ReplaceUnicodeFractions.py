# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import six

_TRANSLATION_TABLE = {
  '¼': '(1/4)',
  '½': '(1/2)',
  '¾': '(3/4)',
  '⅓': '(1/3)',
  '⅔': '(2/3)',
  '⅕': '(1/5)',
  '⅖': '(2/5)',
  '⅗': '(3/5)',
  '⅘': '(4/5)',
  '⅙': '(1/6)',
  '⅚': '(5/6)',
  '⅛': '(1/8)',
  '⅜': '(3/8)',
  '⅝': '(5/8)',
  '⅞': '(7/8)',
  }

def replace_unicode_fractions(s):
    if isinstance(s, six.string_types):
        for k, v in six.iteritems(_TRANSLATION_TABLE):
            s = s.replace(k, v)
    return s
