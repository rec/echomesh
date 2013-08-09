from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import CommandFile
from echomesh.base import Path
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def contexts(_):
  parts = zip(CommandFile.COMMAND_PATH_NAMES, CommandFile.COMMAND_PATH)
  con = ('  %s:\n    %s' % (x, os.path.abspath(y)) for x, y in parts)
  LOGGER.info('%s\n', '\n'.join(con))

HELP = """
In order to control multiple machines and configurations effectively, echomesh
configurations and scores live in one of five different types of "contexts".

default:
  This is the default context that comes with echomesh and contains only the
  default configuration, which cannot be changed by echomesh programs.

master:
  This is the master context which contains your master score.  Most of your
  work will be done here.

platform:
  The platform context contains scores that are specific to platform of the
  machine that echomesh is running on, i.e the operating system and hardware.

  Right now, we have three platforms:  linux, darwin and windows.

tag:
  At configuration time, you can specify text tags for each machine.

name:
  This directory contains scores that are only associated with a machine with
  the given name.

"""
