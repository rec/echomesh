from libcpp.string cimport string
from libcpp cimport bool
from libcpp.string cimport string

include "echomesh/component/InstrumentGrid.pyx"

cdef extern from "Python.h":
   char* PyByteArray_AsString(object bytearray) except NULL


cdef extern from "echomesh/component/LightingWindow.h" namespace "echomesh":
  cdef cppclass LightingWindow:
    InstrumentGrid* grid()
    void saveSnapshotToFile(string)

  LightingWindow* makeLightingWindow()
  void deleteLightingWindow(LightingWindow*) nogil


cdef class PyLightingWindow:
  cdef LightingWindow* thisptr

  def __cinit__(self):
    self.thisptr = makeLightingWindow()

  def __dealloc__(self):
    self.close()

  def close(self):
    deleteLightingWindow(self.thisptr)
    self.thisptr = NULL

  def set_lights(self, object lights):
    self.thisptr.grid().setLights(PyByteArray_AsString(lights))

  def set_light_count(self, int count):
    self.thisptr.grid().setLightCount(count)

  def save_snapshot_to_file(self, object filename):
    self.thisptr.saveSnapshotToFile(filename)
