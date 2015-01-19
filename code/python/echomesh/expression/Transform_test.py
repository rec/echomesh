from __future__ import absolute_import, division, print_function, unicode_literals

import math

from echomesh.Cechomesh import cechomesh

from echomesh.expression import Transform
from echomesh.util.TestCase import TestCase

class TransformTest(TestCase):
    def assertTransform(self, tr):
        s, t = tr
        self.assertNear(s(0), 0)
        self.assertNear(t(0), 0)
        self.assertNear(s(1), 1)
        self.assertNear(t(1), 1)

        VALUES = 0, 1, 0.5, 1 / 3, 2 / 3
        for v in VALUES:
            self.assertNear(v, s(t(v)))
            self.assertNear(v, t(s(v)))

    def test_identity(self):
        self.assertTransform(Transform.IDENTITY)

    def test_square(self):
        self.assertTransform(Transform.SQUARE)

    def test_cube(self):
        self.assertTransform(Transform.power(3))

    def test_sine(self):
        self.assertTransform(Transform.SINE)

    def test_exp(self):
        self.assertTransform(Transform.EXP)

class CTransformTest(TestCase):
    def assertTransform(self, name):
        tr = cechomesh.Transform(name)
        self.assertNear(tr.apply(0), 0)
        self.assertNear(tr.inverse(0), 0)
        self.assertNear(tr.apply(1), 1)
        self.assertNear(tr.inverse(1), 1)

        VALUES = 0, 1, 0.5, 1 / 3, 2 / 3
        for v in VALUES:
            self.assertNear(v, tr.apply(tr.inverse(v)))
            self.assertNear(v, tr.inverse(tr.apply(v)))

    def test_identity(self):
        self.assertTransform("identity")

    def test_square(self):
        self.assertTransform("square")

    def test_cube(self):
        self.assertTransform("cube")

    def test_sine(self):
        self.assertTransform("sine")

    def test_exp(self):
        self.assertTransform("exp")

class FunctionTest(TestCase):
    def assert_function(self, desc):
        f = cechomesh.Function(desc)
        self.assertNear(f(0), 0)
        self.assertNear(f(1), 1)
        return f

    def assert_functions_near(self, d1, d2):
        f1 = cechomesh.Function(d1)
        f2 = cechomesh.Function(d2)
        for x in range(11):
            r = x / 10.0
            self.assertNear(f1(r), f2(r))

    def assert_functions_inverse(self, d1, d2):
        f1 = cechomesh.Function(d1)
        f2 = cechomesh.Function(d2)
        for x in range(11):
            r = x / 10.0
            self.assertNear(f1(f2(r)), r)
            self.assertNear(f2(f1(r)), r)

    def test_identity(self):
        f = self.assert_function('identity')
        self.assertNear(f(0.5), 0.5)

    def test_square(self):
        f = self.assert_function('square')
        self.assertNear(f(0.5), 0.25)

    def test_mirror(self):
        self.assert_functions_near('mirror(identity)', 'identity')
        f = self.assert_function('mirror(square)')
        self.assertNear(f(0.5), 0.5)
        self.assertNear(f(0.25), 0.125)
        self.assertNear(f(0.75), 0.875)

    def test_inverse(self):
        for name in 'square', 'cube', 'log', 'sine':
            self.assert_functions_inverse(name, 'inverse(%s)' % name)


#
