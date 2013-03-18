# from __future__ import absolute_import, division, print_function, unicode_literals

# import copy

# from collections import namedtuple

# class Rect(namedtuple('Rect', ['top_left', 'dimensions'])):
#   """Represents a 2-d rectangle in space.
#   """

#   def bottom_right(self):
#     return self.top_left + self.dimensions

#   def empty(self):
#     return self.dimensions.empty()

#   def union(self, rect):
#     if not rect or rect.empty():
#       rect = self
#     top_left = self.top_left.min(rect.top_left)
#     bottom_right = self.bottom_right().min(rect.bottom_right())
#     return Rect(top_left, bottom_right - top_left)

# def union(r1, r2):
#   return r1.union(r2) if r1 else copy.copy(r2)
