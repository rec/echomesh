# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression import Convert
from echomesh.expression import Expression
from echomesh.util.TestCase import TestCase

class UnitsTest(TestCase):
    EPSILON = 0.0000000000000001

    def test_number(self):
        self.assertNear(Expression.convert(12), 12)

    def test_string(self):
        self.assertNear(Expression.convert('12'), 12)

    def test_unit(self):
        self.assertNear(Expression.convert('12 db'), 3.9810717055349722)

    def test_unit_no_space(self):
        self.assertNear(Expression.convert('12dB'), 3.9810717055349722)

    def test_semitones(self):
        self.assertNear(Expression.convert('10 semitones'), 1.7817974362806785)

    def test_negative(self):
        self.assertNear(Expression.convert('-1 semitone'), 0.9438743126816935)

    def test_cents(self):
        self.assertNear(Expression.convert('50 cents'), 1.029302236643492)

    def test_cent(self):
        self.assertNear(Expression.convert('50 cent'), 1.029302236643492)

    def test_exponential(self):
        self.assertNear(Expression.convert('-1.034E+2 semitones'),
                        0.0025475626362608667)

    def test_negative_decimal(self):
        self.assertNear(Expression.convert('-103.4 semitones'),
                        0.0025475626362608667)

    def test_ms(self):
        self.assertNear(Expression.convert('10ms'), 0.01)

    def test_zero_not_time(self):
        self.assertIs(Convert.convert_time('0'), None)

    def test_zero_not_time2(self):
        self.assertIs(Convert.convert_time('0'), None)

    def test_time_zero(self):
        self.assertNear(Convert.convert_time('0:00'), 0)

    def test_time_one(self):
        self.assertNear(Convert.convert_time('0:01'), 1)

    def test_time_one_minute(self):
        self.assertNear(Convert.convert_time('0:01:00'), 60)

    def test_time_one_hour(self):
        self.assertNear(Convert.convert_time('0:01:00.12'), 60.12)

    def test_time_one_hour_and_change(self):
        self.assertNear(Convert.convert_time('1:01:00.12'), 3660.12)

    def test_addition(self):
        self.assertNear(Expression.convert('13 + 12 ms'), 0.025)

    def test_fraction(self):
        self.assertNear(Expression.convert('1/2sec'), 0.5)

    def test_fraction_and_paren(self):
        self.assertNear(Expression.convert('(1/2)sec'), 0.5)

    def test_unicode_fraction(self):
        self.assertNear(Expression.convert('½sec'), 0.5)

    def test_hz(self):
        self.assertNear(Expression.convert('1Hz'), 1.0)

    def test_ten_hz(self):
        self.assertNear(Expression.convert('10 hertz'), 0.1)

    def test_ten_khz(self):
        self.assertNear(Expression.convert('10 kilohertz'), 0.0001)
