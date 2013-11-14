# distutils: language = c++
# distutils: sources = Source/Tiny.cpp

cdef extern from "Source/Tiny.h" namespace "echomesh":
  cdef cppclass Tiny:
    void show()
    void hide()

cdef extern from "Source/echomesh/EchomeshApplication.h" namespace "echomesh":
  ctypedef void (*Callback)(void *user_data)
  void startApplication(Callback cb, void* user_data)
  void stopApplication()

def start_application(f):
  startApplication(callback, <void*>f)

def stop_application():
  stopApplication()


cdef class TinyWindow:
  cdef Tiny *thisptr

  def __cinit__(self):
    self.thisptr = new Tiny()

  def hide(self):
    self.thisptr.hide()

  def show(self):
    self.thisptr.show()

cdef void callback(void* f):
  (<object>f)()

