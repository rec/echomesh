cdef extern from "echomesh/util/InitLog.h" namespace "echomesh":
  void initLog()
  void setLogger(int logLevel, StringCaller caller, void* callback)

def init_log():
  initLog()

def set_logger(level, callback):
  if callback:
    setLogger(level, perform_string_callback, <void*> callback)
  else:
    setLogger(level, NULL, NULL)
