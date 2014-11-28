from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import Color, interpolate_hue

from echomesh.util.TestCase import TestCase

class ColorTest(TestCase):
    def assertEqualList(self, l1, l2):
        assert len(l1) == len(l2)
        for i, j in zip(l1, l2):
            self.assertNear(i, j)

    def test_empty_color(self):
        self.assertEqual(str(Color()), 'black')

    def test_black(self):
        self.assertEqual(str(Color('black')), 'black')

    def test_red(self):
        self.assertEqual(str(Color('red')), 'red')

    def test_red2(self):
        self.assertEqual(str(Color([1.0, 0, 0])), 'red')

    def test_grey(self):
        FAILS = 1255, 1265, 2555, 5045, 5085
        for i in xrange(100, 9995):
            if i in FAILS:
                continue
            s = 'grey ' + str(i / 100)
            c = str(Color(s))
            if i in range(3325, 3335):
                self.assertEqual(c, 'dark grey')
            elif i in range(4115, 4125):
                self.assertEqual(c, 'dim grey')
            elif i in range(5015, 5025):
                self.assertEqual(c, 'grey')
            elif i in range(7525, 7535):
                self.assertEqual(c, 'silver')
            elif i in range(8265, 8275):
                self.assertEqual(c, 'light grey')
            elif i in range(8625, 8635):
                self.assertEqual(c, 'gainsboro')
            elif i in range(9605, 9615):
                self.assertEqual(c, 'white smoke')
            else:
                f = round(float(c[5:]) * 10) / 10
                g = round(i / 10) / 10
                self.assertEqual(f, g)

        self.assertEquals(Color('grey 0.0'), Color('black'))
        self.assertEquals(Color('grey 100.0'), Color('white'))

    def test_equal(self):
        self.assertEqual(Color('red'), Color('red'))

    def test_unnamed(self):
        self.assertEqual(str(Color([0.7, 0.1, 0.2])),
                         '[red=0.700, green=0.100, blue=0.200]')

    def test_rgb(self):
        self.assertEqual(Color('red').rgb, [1.0, 0.0, 0.0])
        self.assertEqual(Color('red').hsb, [0.0, 1.0, 1.0])
        self.assertEqual(Color('green').rgb, [0.0, 1.0, 0.0])
        self.assertNear(Color('green').hsb, [1.0 / 3.0, 1.0, 1.0])
        self.assertEqual(Color('blue').rgb, [0.0, 0.0, 1.0])
        self.assertNear(Color('blue').hsb, [2.0 / 3.0, 1.0, 1.0])

    def test_hsb(self):
        if False:
            # TODO: come up with a constructor for colors that accepts hsb.
            self.assertEqual(Color('red', model='hsb').rgb, [1.0, 0.0, 0.0])
            self.assertEqual(Color('red', model='hsb').hsb, [0.0, 1.0, 1.0])
            self.assertEqual(Color('green', model='hsb').rgb, [0.0, 1.0, 0.0])
            self.assertNear(
                Color('green', model='hsb').hsb, [1.0 / 3.0, 1.0, 1.0])
            self.assertEqual(Color('blue', model='hsb').rgb, [0.0, 0.0, 1.0])
            self.assertNear(
                Color('blue', model='hsb').hsb, [2.0 / 3.0, 1.0, 1.0])

    def test_unknown(self):
        self.assertRaises(ValueError, Color, 'glug')

    def test_sort2(self):
        self.assertTrue(Color('blue') < Color('green'))

    def test_sort6(self):
        self.assertTrue(Color('blue') < Color('red'))

    def test_sort9(self):
        self.assertTrue(Color('green') < Color('red'))

    def test_interpolate_hue1(self):
        self.assertNear(interpolate_hue(0, 0, 0), 0)
        self.assertNear(interpolate_hue(0, 0, 0.5), 0)
        self.assertNear(interpolate_hue(0, 0, 1.0), 0)

    def test_interpolate_hue2(self):
        self.assertNear(interpolate_hue(0, 0.5, 0), 0)
        self.assertNear(interpolate_hue(0, 0.5, 0.5), 0.25)
        self.assertNear(interpolate_hue(0, 0.5, 1), 0.5)

    def test_interpolate_hue3(self):
        self.assertNear(interpolate_hue(0, 0.6, 0), 0)
        self.assertNear(interpolate_hue(0, 0.6, 0.5), 0.80)
        self.assertNear(interpolate_hue(0, 0.6, 1), 0.6)

    def test_interpolate_hue4(self):
        self.assertNear(interpolate_hue(0.4, 0, 0), 0.4)
        self.assertNear(interpolate_hue(0.4, 0, 0.4), 0.24)
        self.assertNear(interpolate_hue(0.4, 0, 0.6), 0.16)

    def test_interpolate_hue5(self):
        self.assertNear(interpolate_hue(0.8, 0.2, 0.0), 0.8)
        self.assertNear(interpolate_hue(0.8, 0.2, 0.4), 0.96)
        self.assertNear(interpolate_hue(0.8, 0.2, 0.6), 0.04)
