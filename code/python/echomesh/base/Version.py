import sys

TOO_OLD = False
TOO_NEW = False
MAJOR = '?'
MINOR = '?'
IS_26 = False
IS_27 = False
ERROR = ''

_TOO_OLD_ERROR = """
Your version of Python (%s.%s) is too old to run echomesh.
"""

_TOO_NEW_ERROR = """
Your version of Python (%s.%s) is newer than we have tested.
Please proceed with caution.
"""

try:
    MAJOR, MINOR = sys.version_info[:2]
    if MAJOR > 2:
        TOO_NEW = True
    elif MAJOR < 2 or (MAJOR == 2 and MINOR < 6):
        TOO_OLD = True
    else:
        IS_27 = MINOR == 7
        IS_26 = MINOR == 6

except:
    TOO_OLD = True

if TOO_OLD:
    ERROR = _TOO_OLD_ERROR % (MAJOR, MINOR)
elif TOO_NEW:
    ERROR = _TOO_NEW_ERROR % (MAJOR, MINOR)
