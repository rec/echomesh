from libcpp.string cimport string
from libcpp cimport bool

cdef extern from "stdlib.h":
  void* realloc(void *ptr, size_t size)


cdef extern from "Python.h":
   char* PyByteArray_AsString(object bytearray) except NULL

cdef extern from "echomesh/base/Echomesh.h" namespace "echomesh":
  cdef cppclass Point:
    Point(int x, int y)

cdef extern from "echomesh/component/InstrumentGrid.h" namespace "echomesh":
  cdef cppclass InstrumentGrid:
    InstrumentGrid()

    void setLights(unsigned char*)
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
  cdef unsigned char* buff
  cdef int count

  def __cinit__(self):
    self.thisptr = makeLightingWindow()
    self.buff = NULL

  def __dealloc__(self):
    self.close()

  def close(self):
    deleteLightingWindow(self.thisptr)
    self.thisptr = NULL

  def set_lights(self, object lights):
    for i in xrange(3 * self.count):
      self.buff[i] = lights[i]
    self.thisptr.grid().setLights(self.buff)

  def set_light_count(self, int count):
    self.count = count
    self.thisptr.grid().setLightCount(count)
    self.buff = <unsigned char*> realloc(self.buff, 3 * count)
