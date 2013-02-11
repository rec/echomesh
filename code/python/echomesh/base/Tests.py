"""
>>> Merge.merge_all({1: 2, 3: 5}, {1: 4, 2: 7})
{1: 4, 2: 7, 3: 5}

>>> Merge.merge_all({1: 2, 3: 5}, {1: 4, 2: 7}, {1: 23, 5: 1000})
{1: 23, 2: 7, 3: 5, 5: 1000}

>>> Merge.merge_all({1: 2, 3: 5})
{1: 2, 3: 5}

# >>> Merge.merge_all()
# {}
"""

from echomesh.base import Merge
