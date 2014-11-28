from __future__ import absolute_import, division, print_function, unicode_literals

def find_comment(s):
    """ Finds the first comment character in the line that isn't in quotes."""
    quote_single, quote_double, was_backslash = False, False, False
    for i, ch in enumerate(s):
        if was_backslash:
            was_backslash = False
        elif ch == '\\':
            was_backslash = True
        elif quote_single:
            if ch == '\'':
                quote_single = False
        elif quote_double:
            if ch == '"':
                quote_double = False
        elif ch == '\'':
            quote_single = True
        elif ch == '"':
            quote_double = True
        elif ch == '#':
            return i

    return -1

def remove_comment(s):
    pos = find_comment(s)
    return s if (pos == -1) else s[0:pos]
