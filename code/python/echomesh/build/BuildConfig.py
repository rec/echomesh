from __future__ import absolute_import, division, print_function

import os.path
import sys

from Cython.Distutils import extension

DEBUG = True

ECHOMESH_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
  os.path.abspath(__file__)))))

from echomesh.base import Platform

class Config(object):
  def __init__(self):
    self.module_name = 'cechomesh'
    self.library_name = '%s.so' % self.module_name
    self.pyx_files = ['cechomesh.pyx']
    self.libraries = ['echomesh', 'pthread', 'glog']

    if DEBUG:
      self.extra_args = {'cython_gdb': True, 'pyrex_gdb': True}
    else:
      self.extra_args = {}

    extra_compile_args = (
      '-I. -x c++ -arch x86_64 -fmessage-length=0 -std=c++11 '
      '-stdlib=libc++ -IJuceLibraryCode -Ibuild/include')

    if Platform.PLATFORM == Platform.MAC:
      extra_link_args = '-framework Cocoa -framework WebKit -framework CoreMidi'

      if DEBUG:
        extra_compile_args += ' -O0 -g -D_DEBUG=1 -DDEBUG=1'
        extra_link_args += ' -g'
        self.echomesh_lib = 'Builds/MacOSX/build/Debug'

      else:
        extra_compile_args += ' -O2'
        self.echomesh_lib = 'Builds/MacOSX/build/Release'

    elif Platform.PLATFORM == Platform.UBUNTU:
      extra_link_args = (
        '-lc++ -L/usr/X11R6/lib/ -lX11 -lXext -lXinerama -lasound '
        '-ldl -lfreetype -lpthread -lrt -lglog')

      if DEBUG:
        extra_compile_args += ' -O0 -g -D_DEBUG=1 -DDEBUG=1'
        extra_link_args += ' -g'
        self.echomesh_lib = 'Builds/Ubuntu/build'

      else:
        extra_compile_args += ' -02'
        self.echomesh_lib = 'Builds/Ubuntu/build/Release'

    self.extra_compile_args = extra_compile_args.split()
    self.extra_link_args = extra_link_args.split()
    self.bin_dir = os.path.join(ECHOMESH_BASE, 'bin', Platform.PLATFORM)
    self.lib_dirs = ['build/lib', self.echomesh_lib]

    self.extension = extension.Extension(
      self.module_name,
      self.pyx_files,
      library_dirs=self.lib_dirs,
      libraries=self.libraries,
      extra_compile_args=self.extra_compile_args,
      extra_link_args=self.extra_link_args,
      **self.extra_args)


CONFIG = Config()
