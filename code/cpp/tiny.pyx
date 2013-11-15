cdef extern from "Tiny.h" namespace "echomesh":
  cdef cppclass Tiny:
    void show()
    void hide()

  string tinyTest()

# cdef class AudioPlayer

cdef class TinyWindow:
  cdef Tiny *thisptr

  def __cinit__(self):
    self.thisptr = new Tiny()

  def hide(self):
    self.thisptr.hide()

  def show(self):
    self.thisptr.show()

