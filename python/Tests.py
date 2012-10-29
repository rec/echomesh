"""

>>> String.truncate('hello', 6)
u'hello'

>>> String.truncate('hello', 5)
u'hello'

>>> String.truncate('hello', 4)
u'h...'

>>> String.truncate('hello', 3)
u'...'

>>> String.truncate('hello', 2)
u'..'

>>> String.truncate('hello', 1)
u'.'

>>> String.truncate('hello', 0)
u''

>>> String.truncate_suffix('hello', ' suf', 9)
u'hello suf'

>>> String.truncate_suffix('hello', ' suf', 8)
u'h... suf'

>>> String.truncate_suffix('hello', ' suf', 7)
u'... suf'

>>> String.truncate_suffix('hello', ' suf', 6)
u'.. suf'

>>> String.truncate_suffix('hello', ' suf', 5)
u'. suf'

>>> String.truncate_suffix('hello', ' suf', 4)
u' suf'

>>> cb = Util.call_if_different(print)

>>> cb(1)
1

>>> cb(1)

>>> cb(2)
2

>>> cb(1)
1

>>> env = Envelope.Envelope([[0, 5.0], [1, 10.0], [2, 20.0]])

>>> env.interpolate(-1)
5.0

>>> env.interpolate(0)
5.0

>>> env.interpolate(0.5)
7.5

>>> env.interpolate(1)
10.0

>>> env.interpolate(1.5)
15.0

>>> env.interpolate(2)
20.0

>>> env.interpolate(3)
20.0

>>> env2 = Envelope.Envelope([[0, [5.0, 50.0]], [1, [10.0, 100.0]], [2, [20.0, 200.0]]])

>>> env2.interpolate(-1)
[5.0, 50.0]

>>> env2.interpolate(0)
[5.0, 50.0]

>>> env2.interpolate(0.5)
[7.5, 75.0]

>>> env2.interpolate(1)
[10.0, 100.0]

>>> env2.interpolate(1.5)
[15.0, 150.0]

>>> env2.interpolate(2)
[20.0, 200.0]

>>> env2.interpolate(3)
[20.0, 200.0]

>>> list(Average.average(range(8), moving=2))
[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]

>>> list(Average.average(range(8), grouped=2))
[0.5, 2.5, 4.5, 6.5]

>>> list(Average.average(range(8), grouped=2, moving=2))
[1.5, 3.5, 5.5]

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from util import Average
from util import Envelope
from util import Merge
from util import String
from util import Util

if __name__ == "__main__":
  import doctest
  doctest.testmod()
