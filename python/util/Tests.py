from __future__ import absolute_import, division, print_function, unicode_literals

"""

>>> Util.truncate('hello', 6)
'hello'

>>> Util.truncate('hello', 5)
'hello'

>>> Util.truncate('hello', 4)
'h...'

>>> Util.truncate('hello', 3)
'...'

>>> Util.truncate('hello', 2)
'..'

>>> Util.truncate('hello', 1)
'.'

>>> Util.truncate('hello', 0)
''

>>> Util.truncate_suffix('hello', ' suf', 9)
'hello suf'

>>> Util.truncate_suffix('hello', ' suf', 8)
'h... suf'

>>> Util.truncate_suffix('hello', ' suf', 7)
'... suf'

>>> Util.truncate_suffix('hello', ' suf', 6)
'.. suf'

>>> Util.truncate_suffix('hello', ' suf', 5)
'. suf'

>>> Util.truncate_suffix('hello', ' suf', 4)
' suf'


>>> import mock
>>> mock_open = mock.mock_open()

>>> Util.get_and_increment_index_file('/tmp/test.txt', mock_open)
'0'

"""

import Util

if __name__ == "__main__":
  import doctest
  doctest.testmod()
