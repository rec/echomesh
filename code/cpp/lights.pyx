from libcpp.string cimport string
from libcpp cimport bool

cdef extern from "Python.h":
   char* PyByteArray_AsString(object bytearray) except NULL

cdef extern from "echomesh/base/Echomesh.h" namespace "echomesh":
  cdef cppclass Point:
    Point(int x, int y)

cdef extern from "echomesh/component/InstrumentGrid.h" namespace "echomesh":
  cdef cppclass InstrumentGrid:
    InstrumentGrid()

    void setLights(char*)
    void setPaintingIsUnclipped(bool)
    void setLightCount(int)
    void setLabelStartsAtZero(bool)
    void setLayout(Point layout, Point size, Point padding,
                   Point instrumentPadding, Point labelPadding)
    void setShowLabel(bool)
    void doRepaint()
    int getLightCount()

cdef extern from "echomesh/component/LightingWindow.h" namespace "echomesh":
  cdef cppclass LightingWindow:
    InstrumentGrid* grid()

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
