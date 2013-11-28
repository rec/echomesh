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
