"""
>>> Merge.merge({1: 2, 3: 5}, {1: 4, 2: 7})
{1: 4, 2: 7, 3: 5}

>>> Merge.merge({1: 2, 3: 5}, {1: 4, 2: 7}, {1: 23, 5: 1000})
{1: 23, 2: 7, 3: 5, 5: 1000}

>>> Merge.merge({1: 2, 3: 5})
{1: 2, 3: 5}

# >>> Merge.merge()
# {}
"""

from echomesh.base import Merge
