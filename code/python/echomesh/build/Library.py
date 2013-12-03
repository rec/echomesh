from __future__ import absolute_import, division, print_function, unicode_literals

import os

from distutils.core import Command
from echomesh.base import Platform
from echomesh.build.BuildConfig import CONFIG
from echomesh.build.CleanOlder import clean_older
from echomesh.build.Execute import execute_command

class Library(Command):
  description = 'Build C++ library'
  user_options = []
  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    execute_command('library')
    clean_older()
