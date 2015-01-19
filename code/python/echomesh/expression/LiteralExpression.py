from __future__ import absolute_import, division, print_function, unicode_literals

class LiteralExpression(object):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def is_constant(self):
        return True

    def __str__(self):
        return 'LiteralExpression(%s)' % self.value
