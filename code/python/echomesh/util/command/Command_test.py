from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.command import Command
from echomesh.util.TestCase import TestCase

class Command_test(TestCase):
    def test_simple(self):
        registry = Command.Registry('test', 'echomesh.util.command.test', '')
        foo = registry['f']
        self.assertEquals(foo(), 'foo')
        self.assertEquals(registry.help('foo'), 'Some help text')

    def test_two(self):
        registry = Command.Registry('test', 'echomesh.util.command.test',
                                    'echomesh.util.command.test.Baz')
        foo = registry['f']
        self.assertEquals(foo(), 'foo')
        with self.assertRaises(KeyError) as cm:
            b = registry['ba']
        self.assertEquals(
            str(cm.exception),
            'In table test, "ba" matches more than one: bar and baz')
        self.assertEquals(registry['baz'](), 'baz')
