"""

>>> SizeName.size_name(0)
u'0'

>>> SizeName.size_name(1023)
u'1023'

>>> SizeName.size_name(1024)
u'1K'

>>> SizeName.size_name(1023 * 1024)
u'1023K'

>>> SizeName.size_name(1023 * 1024 + 511)
u'1023K'

>>> SizeName.size_name(1023 * 1024 + 512)
u'1M'

>>> SizeName.size_name(1024 * 1024 - 1)
u'1M'

>>> SizeName.size_name(1024 * 1024)
u'1M'

>>> SizeName.size_name(1024 * 1024 * 1024)
u'1G'

>>> SizeName.size_name(1024 * 1024 * 1024)
u'1G'

"""

from echomesh.util import SizeName
