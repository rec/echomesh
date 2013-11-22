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

def init_log():
  initLog()

