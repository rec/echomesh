from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

PERM_ERROR = """
%s needs to be run as superuser because
%s

Please rerun it as follows:

  sudo %s
"""

def test_superuser(reason, program_name='echomesh'):
    if os.geteuid():
        raise Exception(PERM_ERROR % (program_name, reason, ' '.join(sys.argv)))
