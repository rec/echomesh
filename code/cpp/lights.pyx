from libcpp.string cimport string

cdef extern from "Python.h":
   char* PyByteArray_AsString(object bytearray) except NULL

cdef extern from "echomesh/base/Config.h" namespace "echomesh":
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
    LightingWindow()
    InstrumentGrid* grid()

cdef class PyLightingWindow:
  cdef LightingWindow* thisptr

  def __cinit__(self):
    self.thisptr = new LightingWindow()

  def __dealloc__(self):
    del self.thisptr

  def set_lights(self, object lights):
    self.thisptr.grid().setLights(PyByteArray_AsString(lights))

