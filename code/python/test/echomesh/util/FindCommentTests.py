"""
>>> remove_comment('hello world')
u'hello world'

>>> remove_comment('hello world #')
u'hello world '

>>> remove_comment('hello world \\#')
u'hello world \\\\#'

>>> remove_comment('hello world " # not a comment" # comment')
u'hello world " # not a comment" '

>>> remove_comment("hello world ' # not a comment' # comment")
u"hello world ' # not a comment' "

>>> remove_comment(HARD_ONE)
u'hello world "this # is #\\' it" \\'# not\\' '
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.string.FindComment import remove_comment

HARD_ONE = """hello world "this # is #' it" '# not' # comment"""
