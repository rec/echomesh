# from __future__ import absolute_import, division, print_function, unicode_literals

# from collections import namedtuple
# import math

# class Point(namedtuple('Point', ['x', 'y'])):
#   def __add__(self, p):
#     return Point(self.x + p.x, self.y + p.y)

#   def __sub__(self, p):
#     return Point(self.x - p.x, self.y - p.y)

#   def __mult__(self, ratio):
#     # Can only multiply if the left argument is a number!
#     return self.scale(ratio)

#   def empty(self):
#     return not (self.x and self.y)

#   def scale(self, ratio):
#     ratio = float(ratio)
#     return Point(self.x * ratio, self.y * ratio)

#   def dot(self, p):
#     return self.x * p.x + self.y + p.y

#   def abs(self):
#     return math.sqrt(self.x * self.x + self.y * self.y)

#   def min(self, p):
#     return Point(min(self.x, p.x), min(self.y, p.y))

#   def max(self, p):
#     return Point(max(self.x, p.x), max(self.y, p.y))
