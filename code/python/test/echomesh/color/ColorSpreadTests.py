"""
>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 0)
array([], shape=(0, 3), dtype=float64)

>>> ColorSpread.color_spread([1, 0, 0], [0, 0, 1], 6)
array([[ 1. ,  0. ,  0. ],
       [ 1. ,  0.8,  0. ],
       [ 0.4,  1. ,  0. ],
       [ 0. ,  1. ,  0.4],
       [ 0. ,  0.8,  1. ],
       [ 0. ,  0. ,  1. ]])

>>> ColorSpread.color_spread([1, 0, 0], [0, 0, 1], 6, use_hsv=False)
array([[ 1. ,  0. ,  0. ],
       [ 0.8,  0. ,  0.2],
       [ 0.6,  0. ,  0.4],
       [ 0.4,  0. ,  0.6],
       [ 0.2,  0. ,  0.8],
       [ 0. ,  0. ,  1. ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6)
array([[ 1. ,  1. ,  0. ],
       [ 0.6,  1. ,  0. ],
       [ 0.2,  1. ,  0. ],
       [ 0. ,  1. ,  0.2],
       [ 0. ,  1. ,  0.6],
       [ 0. ,  1. ,  1. ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, Transform.IDENTITY)
array([[ 1. ,  1. ,  0. ],
       [ 0.6,  1. ,  0. ],
       [ 0.2,  1. ,  0. ],
       [ 0. ,  1. ,  0.2],
       [ 0. ,  1. ,  0.6],
       [ 0. ,  1. ,  1. ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, transform=Transform.SQUARE)
array([[ 1.        ,  1.        ,  0.        ],
       [ 0.38754845,  1.        ,  0.        ],
       [ 0.        ,  1.        ,  0.04939015],
       [ 0.        ,  1.        ,  0.40831892],
       [ 0.        ,  1.        ,  0.7202941 ],
       [ 0.        ,  1.        ,  1.        ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, transform=Transform.power(2))
array([[ 1.        ,  1.        ,  0.        ],
       [ 0.38754845,  1.        ,  0.        ],
       [ 0.        ,  1.        ,  0.04939015],
       [ 0.        ,  1.        ,  0.40831892],
       [ 0.        ,  1.        ,  0.7202941 ],
       [ 0.        ,  1.        ,  1.        ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, transform=Transform.inverse(Transform.SQUARE))
array([[ 1.        ,  1.        ,  0.        ],
       [ 0.68574374,  1.        ,  0.        ],
       [ 0.32861561,  1.        ,  0.        ],
       [ 0.        ,  1.        ,  0.07138439],
       [ 0.        ,  1.        ,  0.51425626],
       [ 0.        ,  1.        ,  1.        ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, transform=Transform.inverse(Transform.SQUARE))
array([[ 1.        ,  1.        ,  0.        ],
       [ 0.68574374,  1.        ,  0.        ],
       [ 0.32861561,  1.        ,  0.        ],
       [ 0.        ,  1.        ,  0.07138439],
       [ 0.        ,  1.        ,  0.51425626],
       [ 0.        ,  1.        ,  1.        ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, transform=Transform.EXP)
array([[ 1.        ,  1.        ,  0.        ],
       [ 0.54311082,  1.        ,  0.        ],
       [ 0.11856458,  1.        ,  0.        ],
       [ 0.        ,  1.        ,  0.27791662],
       [ 0.        ,  1.        ,  0.64981435],
       [ 0.        ,  1.        ,  1.        ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, transform=Transform.inverse(Transform.EXP))
array([[ 1.        ,  1.        ,  0.        ],
       [ 0.65665603,  1.        ,  0.        ],
       [ 0.28706791,  1.        ,  0.        ],
       [ 0.        ,  1.        ,  0.11077039],
       [ 0.        ,  1.        ,  0.53901822],
       [ 0.        ,  1.        ,  1.        ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, transform=Transform.SINE)
array([[ 1.        ,  1.        ,  0.        ],
       [ 0.46179262,  1.        ,  0.        ],
       [ 0.04354821,  1.        ,  0.        ],
       [ 0.        ,  1.        ,  0.3244033 ],
       [ 0.        ,  1.        ,  0.66752594],
       [ 0.        ,  1.        ,  1.        ]])

>>> ColorSpread.color_spread([1, 1, 0], [0, 1, 1], 6, transform=Transform.inverse(Transform.SINE))
array([[ 1.        ,  1.        ,  0.        ],
       [ 0.65355085,  1.        ,  0.        ],
       [ 0.27194337,  1.        ,  0.        ],
       [ 0.        ,  1.        ,  0.13670856],
       [ 0.        ,  1.        ,  0.56371608],
       [ 0.        ,  1.        ,  1.        ]])

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorSpread
from echomesh.expression import Transform
