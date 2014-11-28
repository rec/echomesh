from __future__ import absolute_import, division, print_function, unicode_literals

import os

from distutils.core import Command
from echomesh.build.BuildConfig import CONFIG
from echomesh.build.Execute import execute, execute_command

class Clean(Command):
    description = 'Complete clean command'
    user_options = []
    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        execute('rm -Rf %s.so ./build/temp* ./dist echomesh.cpp' %
                  CONFIG.module_name)
        execute_command('clean')
