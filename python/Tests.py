"""

>>> Util.truncate('hello', 6)
u'hello'

>>> Util.truncate('hello', 5)
u'hello'

>>> Util.truncate('hello', 4)
u'h...'

>>> Util.truncate('hello', 3)
u'...'

>>> Util.truncate('hello', 2)
u'..'

>>> Util.truncate('hello', 1)
u'.'

>>> Util.truncate('hello', 0)
u''

>>> Util.truncate_suffix('hello', ' suf', 9)
u'hello suf'

>>> Util.truncate_suffix('hello', ' suf', 8)
u'h... suf'

>>> Util.truncate_suffix('hello', ' suf', 7)
u'... suf'

>>> Util.truncate_suffix('hello', ' suf', 6)
u'.. suf'

>>> Util.truncate_suffix('hello', ' suf', 5)
u'. suf'

>>> Util.truncate_suffix('hello', ' suf', 4)
u' suf'

>>> levels = [2, 3, 5]

>>> Util.level_slot(0, levels)
0

>>> Util.level_slot(2, levels)
1

>>> Util.level_slot(3, levels)
2

>>> Util.level_slot(4, levels)
2

>>> Util.level_slot(5, levels)
3

>>> Util.level_slot(6, levels)
3

>>> cb = Util.call_if_different(print)

>>> cb(1)
1

>>> cb(1)

>>> cb(2)
2

>>> cb(1)
1

>>> import mock
>>> mock_open = mock.mock_open()

>>> Util.get_and_increment_index_file('/tmp/test.txt', mock_open)
u'0'

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from util import Util

if __name__ == "__main__":
  import doctest
  doctest.testmod()
