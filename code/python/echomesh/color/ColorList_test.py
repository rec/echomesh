from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import Color, ColorList, even_color_spread

from echomesh.util.TestCase import TestCase

class ColorListTest(TestCase):
    def setUp(self):
        self.cl = ColorList()

    def assertResult(self, s):
        self.assertEqual(str(self.cl), s)

    def test_single(self):
        self.cl.append('red')
        self.assertResult('[red]')

    def test_issue(self):
        cl = ColorList(['red', 'white'])
        self.assertEqual(str(cl), '[red, white]')

    def test_issue(self):
        cl = ColorList(['red', 'white', 'green', 'blue'])
        self.assertEqual(str(cl), '[red, white, green, blue]')

    def test_single_hsb(self):
        self.cl = ColorList()
        self.cl.append('red')
        self.assertResult('[red]')

    def test_empty(self):
        self.assertResult('[]')

    def test_append(self):
        self.cl.append('red')
        self.assertResult('[red]')
        self.assertRaises(ValueError, self.cl.append, 'glug')
        self.assertResult('[red]')

    def test_sort(self):
        self.cl.extend(['green', 'red', 'blue'])
        self.cl.sort()
        self.assertResult('[blue, green, red]')

    def test_combine(self):
        self.cl.extend(['black', 'white', 'red', 'blue', 'green'])
        self.cl.combine(['white', 'white', 'blue', 'green', 'red'])
        self.assertResult('[white, white, magenta, cyan, yellow]')

    def test_combine_columns(self):
        self.cl = ColorList(['yellow', 'white', 'red', 'blue', 'green'],
                            columns=2)
        self.cl.combine(ColorList(['yellow', 'white', 'black', 'green', 'red'],
                                  columns=3))
        self.assertResult('[\n [yellow, white, black],\n'
                          ' [yellow, magenta, black],\n'
                          ' [green, black, black]]')

    def test_combine_columns2(self):
        self.cl = ColorList(['yellow', 'white', 'red', 'blue', 'green'],
                            columns=3)
        self.cl.combine(ColorList(['yellow', 'white', 'red', 'green', 'coral'],
                                  columns=2))
        self.assertResult('[\n [yellow, white, red],\n'
                          ' [magenta, green, black],\n'
                          ' [coral, black, black]]')

    def test_combine_columns4(self):
        self.cl = ColorList()
        self.cl.combine(ColorList(['yellow', 'white', 'red', 'green', 'coral'],
                                  columns=2))
        self.assertResult('[\n [yellow, white],\n [red, green],\n [coral]]')

    def test_count(self):
        self.cl.extend(['green', 'red', 'blue', 'red', 'pink'])
        self.assertEqual(self.cl.count('green'), 1)
        self.assertEqual(self.cl.count('yellow'), 0)
        self.assertEqual(self.cl.count('red'), 2)

    def test_index(self):
        self.cl.extend(['green', 'red', 'blue', 'red', 0x303030])
        self.assertEqual(self.cl.index('green'), 0)
        self.assertEqual(self.cl.index('red'), 1)
        self.assertRaises(ValueError, self.cl.index, 'yellow')

    def test_insert(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        self.cl.insert(2, 'pink')
        self.assertResult('[green, red, pink, blue, red]')

    def test_slice1(self):
        self.cl[:] = ['green', 'red', 'blue', 'red']
        self.assertResult('[green, red, blue, red]')

    def test_slice2(self):
        self.cl[:] = ['green', 'red', 'blue', 'red']
        self.cl[1:4:2] = ['pink', 'orange']
        self.assertResult('[green, pink, blue, pink]')

    def test_getslice1(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        self.cl = self.cl[:]
        self.assertResult('[green, red, blue, red]')

    def test_getslice1(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        self.cl = self.cl[1::2]
        self.assertResult('[red, red]')

    def test_del(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        del self.cl[2]
        self.assertResult('[green, red, red]')

    def test_del(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        del self.cl[2]
        self.assertResult('[green, red, red]')

    def test_columns(self):
        cl = ColorList(['green', 'red', 'blue'], columns=8)
        cl.columns = 4
        self.assertEqual(
          cl, ColorList(['green', 'red', 'blue', 'black'], columns=4))

        self.cl = ColorList(['green', 'red', 'blue', 'yellow', 'orange'],
                            columns=3)
        self.assertEqual(self.cl, self.cl)
        cl = ColorList(['green', 'red', 'blue', 'yellow', 'orange'], columns=2)
        self.assertNotEqual(self.cl, cl)

        self.cl.columns = 2
        self.assertEqual(
          self.cl, ColorList(['green', 'red', 'yellow', 'orange'], columns=2))

        self.cl.columns = 3
        self.assertEqual(
          self.cl, ColorList(
              ['green', 'red', 'black', 'yellow', 'orange', 'black'],
              columns=3))

    def test_contains(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        self.assertTrue('red' in self.cl)
        self.assertFalse('pink' in self.cl)

    def test_add(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        self.cl = self.cl + ['yellow', 'pink']
        self.assertResult('[green, red, blue, red, yellow, pink]')

    def test_radd(self):
        self.cl.extend(['yellow', 'pink'])
        self.cl = ['green', 'red', 'blue', 'red'] + self.cl
        self.assertResult('[green, red, blue, red, yellow, pink]')

    def test_iadd(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        self.cl += ['yellow', 'pink']
        self.assertResult('[green, red, blue, red, yellow, pink]')

    def test_pop(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        self.assertEqual(self.cl.pop(), Color('red'))
        self.assertEqual(self.cl, ColorList(['green', 'red', 'blue']))
        self.assertEqual(self.cl.pop(0), Color('green'))
        self.assertEqual(self.cl, ColorList(['red', 'blue']))
        self.assertRaises(IndexError, self.cl.pop, 3)

    def test_remove(self):
        self.cl.extend(['green', 'red', 'blue', 'red'])
        self.cl.remove('red')
        self.assertEqual(self.cl, ColorList(['green', 'blue', 'red']))
        self.cl.remove('green')
        self.assertEqual(self.cl, ColorList(['blue', 'red']))
        self.assertRaises(ValueError, self.cl.remove, 'green')

    def test_reverse(self):
        self.cl += ['green', 'red', 'blue', 'red']
        self.cl.reverse()
        self.assertEqual(self.cl, ColorList(['red', 'blue', 'red', 'green']))

    def test_reversed(self):
        self.cl += ['green', 'red', 'blue', 'red']
        cl = reversed(self.cl)
        self.assertEqual(cl, ColorList(['red', 'blue', 'red', 'green']))

    def test_mul(self):
        self.cl += ['green', 'red']
        self.cl = self.cl * 3
        self.assertEqual(
            self.cl,
            ColorList(['green', 'red', 'green', 'red', 'green', 'red']))

    def test_rmul(self):
        self.cl += ['green', 'red']
        self.cl = 3 * self.cl
        self.assertEqual(
            self.cl,
            ColorList(['green', 'red', 'green', 'red', 'green', 'red']))

    def test_imul(self):
        self.cl += ['green', 'red']
        self.cl *= 3
        self.assertEqual(
            self.cl,
            ColorList(['green', 'red', 'green', 'red', 'green', 'red']))

    def test_scale0(self):
        self.cl += ['green', 'red']
        self.cl.scale(0)
        self.assertResult('[black, black]')

    def test_scale1(self):
        self.cl += ['green', 'red']
        self.cl.scale(1)
        self.assertResult('[green, red]')

    def test_scale2(self):
        self.cl += ['white']
        self.cl.scale(0.5)
        self.assertResult('[grey 50]')

    def test_spread1(self):
        self.cl = even_color_spread(2, 'black', 'white')
        self.assertResult('[black, white]')

    def test_spread2(self):
        self.cl = even_color_spread(3, 'black', 'white', 'green')
        self.assertResult('[black, white, green]')

    def test_spread3(self):
        self.cl = even_color_spread(5, 'black', 'white')
        self.assertResult('[black, grey 25, grey 50, grey 75, white]')

    def test_spread4(self):
        self.cl = even_color_spread(5, 'white', 'red')
        self.assertResult('[white, '
                          '[red=1.000, green=0.750, blue=0.750], '
                          '[red=1.000, green=0.500, blue=0.500], '
                          '[red=1.000, green=0.250, blue=0.250], '
                          'red]')

    def test_spread5(self):
        self.cl = even_color_spread(10, 'black', 'white', 'red', 'yellow')
        self.assertResult('[black, dark grey, grey 66.7, white, '
                          '[red=1.000, green=0.667, blue=0.667], '
                          '[red=1.000, green=0.333, blue=0.333], red, '
                          '[red=1.000, green=0.333, blue=0.000], '
                          '[red=1.000, green=0.667, blue=0.000], yellow]')

    def test_spread6(self):
        self.cl = even_color_spread(5, 'black', 'white', 'red')
        self.assertResult('[black, grey 50, white, '
                          '[red=1.000, green=0.500, blue=0.500], red]')
