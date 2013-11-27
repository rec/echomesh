include "callback.pyx"

from libcpp.string cimport string

cdef extern from "echomesh/util/EchomeshApplication.h" namespace "echomesh":
  void startApplication(VoidCaller cb, void* user_data)
  void stopApplication()
  void writeConsole(string)
  void flushConsole()
  void readConsole(StringCaller, void*)

def start_application(f):
  if f:
    startApplication(perform_callback, <void*>f)
  else:
    startApplication(NULL, NULL)

def stop_application():
  stopApplication()

def write(s):
  writeConsole(s)

def flush():
  flushConsole()

def add_read_callback(callback):
  readConsole(perform_string_callback, <void*> callback)

