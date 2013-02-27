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

>>> remove_comment('''hello world "this # is #' it" '# not' # comment''')
u'hello world "this # is #\\' it" \\'# not\\' '
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.FindComment import remove_comment
