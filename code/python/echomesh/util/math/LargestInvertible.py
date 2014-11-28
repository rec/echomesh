from __future__ import absolute_import, division, print_function, unicode_literals

import fractions
import math

from six.moves import xrange

# http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
# from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm

def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a:
        q, r = b // a, b % a
        m, n = x - u*q, y - v*q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g == 1:
        return x % m
    raise Exception('modular inverse does not exist')

def largest_invertible(x):
    """In the ring Mod(x), returns the invertible number nearest to x / 2, and
       its inverse."""
    if x >= 5:
        for i in xrange(int(x / 2), 1, -1):
            try:
                ii = (i if i < (x / 2) else x - i)
                return ii, modinv(ii, x)
            except:
                pass

    return 1, 1
