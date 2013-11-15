# distutils: language = c++
# distutils: sources = Tiny.cpp

cdef extern from "Tiny.h" namespace "echomesh":
  cdef cppclass Tiny:
    void show()
    void hide()

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


# cdef class AudioPlayer

cdef class TinyWindow:
  cdef Tiny *thisptr

  def __cinit__(self):
    self.thisptr = new Tiny()

  def hide(self):
    self.thisptr.hide()

  def show(self):
    self.thisptr.show()

