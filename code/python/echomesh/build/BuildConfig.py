from __future__ import absolute_import, division, print_function

import os.path
import sys

from Cython.Build import cythonize
from Cython.Distutils import extension

_DEBUG_FLAG = '--debug'

DEBUG = _DEBUG_FLAG in sys.argv
if DEBUG:
  sys.argv.remove(_DEBUG_FLAG)

VERBOSE = True

ECHOMESH_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
  os.path.dirname(os.path.abspath(__file__))))))

from echomesh.base import Platform

class Config(object):
  def __init__(self):
    self.debug = DEBUG
    self.verbose = VERBOSE
    self.module_name = 'cechomesh'
    self.library_name = '%s.so' % self.module_name
    pyx_files = ['cechomesh.pyx']
    libraries = ['echomesh', 'pthread', 'glog']

    extra_compile_args = (
      '-I. -fmessage-length=0 -std=c++11 '
      ' -IJuceLibraryCode -Ibuild/include ')

    if DEBUG:
      extra_args = {'cython_gdb': True, 'pyrex_gdb': True}
      extra_compile_args += '-O0 -g -D_DEBUG=1 -DDEBUG=1 '
      extra_link_args = '-g '
    else:
      extra_args = {}
      extra_compile_args += '-O2 '
      extra_link_args = ''

    if Platform.PLATFORM == Platform.MAC:
      extra_link_args += '-framework Cocoa -framework WebKit -framework CoreMidi '
      extra_compile_args += '-stdlib=libc++ -arch x86_64  -x c++ '

      if DEBUG:
        echomesh_lib = 'Builds/MacOSX/build/Debug'

      else:
        echomesh_lib = 'Builds/MacOSX/build/Release'

    elif Platform.PLATFORM == Platform.UBUNTU:
      extra_link_args += (
        '-lc++ -L/usr/X11R6/lib/ -lX11 -lXext -lXinerama -lasound '
        '-ldl -lfreetype -lrt ')
      extra_compile_args += '-stdlib=libc++ -arch x86_64  -x c++ '

      if DEBUG:
        echomesh_lib = 'Builds/Linux/build/Debug'

      else:
        echomesh_lib = 'Builds/Linux/build'

    elif Platform.PLATFORM == Platform.DEBIAN:
      extra_link_args += (
        '-lc++ -L/usr/X11R6/lib/ -lX11 -lXext -lXinerama -lasound '
        '-ldl -lfreetype -lrt ')

      if DEBUG:
        echomesh_lib = 'Builds/Linux/build/Debug'

      else:
        echomesh_lib = 'Builds/Linux/build'

    else:
      raise Exception("Don't understand platform %s" % Platform.PLATFORM)

    extra_compile_args = extra_compile_args.split()
    extra_link_args = extra_link_args.split()
    self.bin_dir = os.path.join(ECHOMESH_BASE, 'bin', Platform.PLATFORM)
    lib_dirs = ['build/lib', echomesh_lib]

    ext = extension.Extension(
      self.module_name,
      pyx_files,
      library_dirs=lib_dirs,
      libraries=libraries,
      extra_compile_args=extra_compile_args,
      extra_link_args=extra_link_args,
      **extra_args)

    self.modules = cythonize([ext], **extra_args)
    self.c_library = os.path.join(echomesh_lib, 'libechomesh.a')


CONFIG = Config()