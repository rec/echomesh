from __future__ import absolute_import, division, print_function, unicode_literals

# From here:
# http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type(str('Enum'), (), enums)
