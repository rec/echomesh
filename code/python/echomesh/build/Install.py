from __future__ import absolute_import, division, print_function, unicode_literals

import shutil

from distutils.core import Command
from echomesh.build.BuildConfig import CONFIG

class Install(Command):
    description = 'Install library in bin directory.'
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.copy(CONFIG.library_name, CONFIG.bin_dir)
        if CONFIG.verbose:
            print('Copied %s to %s' % (CONFIG.library_name, CONFIG.bin_dir))
