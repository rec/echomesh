from __future__ import absolute_import, division, print_function, unicode_literals

import re

_MATCH_HASHTAG = re.compile(r'(?:^|\W)#\w\w+')

def remove_hashtags(s):
    split = _MATCH_HASHTAG.split(s)
    join = ''.join(split)
    return join.strip()
