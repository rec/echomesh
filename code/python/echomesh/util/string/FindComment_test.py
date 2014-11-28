from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.string.FindComment import remove_comment
from echomesh.util.TestCase import TestCase

HARD_ONE = """hello world "this # is #' it" '# not' # comment"""

class FindCommentTest(TestCase):
    def test_trivial(self):
        self.assertEqual(remove_comment('hello world'), 'hello world')

    def test_empty_comment(self):
        self.assertEqual(remove_comment('hello world #'), 'hello world ')

    def test_escaped_comment(self):
        self.assertEqual(remove_comment('hello world \\#'), 'hello world \\#')

    def test_quoted_comment(self):
        self.assertEqual(
            remove_comment('hello world " # not a comment" # comment'),
            'hello world " # not a comment" ')

    def test_hard_one(self):
        self.assertEqual(remove_comment(HARD_ONE),
                         'hello world "this # is #\' it" \'# not\' ')
