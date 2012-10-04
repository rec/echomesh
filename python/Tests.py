#!/usr/bin/python

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

>>> Util.truncateSuffix('hello', ' suf', 9)
'hello suf'

>>> Util.truncateSuffix('hello', ' suf', 8)
'h... suf'

>>> Util.truncateSuffix('hello', ' suf', 7)
'... suf'

>>> Util.truncateSuffix('hello', ' suf', 6)
'.. suf'

>>> Util.truncateSuffix('hello', ' suf', 5)
'. suf'

>>> Util.truncateSuffix('hello', ' suf', 4)
' suf'



>>> import mock
>>> mock_open = mock.mock_open()

>>> Util.getAndIncrementIndexFile('/tmp/test.txt', mock_open)
'0'

"""

import Util

if __name__ == "__main__":
  import doctest
  doctest.testmod()
