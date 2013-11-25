include "callback.pyx"

cdef extern from "echomesh/util/EchomeshApplication.h" namespace "echomesh":
  void startApplication(Callback cb, void* user_data)
  void stopApplication()

def start_application(f):
  startApplication(perform_callback, <void*>f)

def stop_application():
  stopApplication()

cdef extern from "echomesh/util/InitLog.h" namespace "echomesh":
  void initLog()
  void setLogger(int logLevel, StringCallback caller, void* callback)

def init_log():
  initLog()

def set_logger(level, callback):
  setLogger(level, perform_string_callback_gil, <void*> callback)
