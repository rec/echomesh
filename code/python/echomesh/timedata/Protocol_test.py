from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.timedata import Protocol
from echomesh.util.TestCase import TestCase

class Protocol_test(TestCase):
    def test_tag(self):
        self.assertFalse(Protocol.is_tag(''))
        self.assertFalse(Protocol.is_tag('no'))
        self.assertFalse(Protocol.is_tag('#'))
        self.assertFalse(Protocol.is_tag('##a'))
        self.assertFalse(Protocol.is_tag('##ab'))

        self.assertTrue(Protocol.is_tag('#a'))
        self.assertTrue(Protocol.is_tag('#ab'))
        self.assertTrue(Protocol.is_tag('#abc'))

        self.assertFalse(Protocol.pop_tag([]))
        self.assertFalse(Protocol.pop_tag(['hello']))
        self.assertFalse(Protocol.pop_tag(['#']))
        self.assertFalse(Protocol.pop_tag(['##']))
        self.assertFalse(Protocol.pop_tag(['hello', '#tag']))

        self.assertEquals(Protocol.pop_tag(['#tag']), '#tag')
        self.assertEquals(Protocol.pop_tag(['#tag', 'hello']), '#tag')

if __name__ == '__main__':
    TestCase.main()
