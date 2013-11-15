cdef extern from "echomesh/util/EchomeshApplication.h" namespace "echomesh":
  ctypedef void (*Callback)(void *user_data)
  void startApplication(Callback cb, void* user_data)
  void stopApplication()

def start_application(f):
  startApplication(callback, <void*>f)

def stop_application():
  stopApplication()

cdef void callback(void* f):
  (<object>f)()


