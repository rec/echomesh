from libcpp.string cimport string
from libcpp cimport bool
from libcpp.string cimport string

include "echomesh/component/InstrumentGrid.pyx"

cdef extern from "echomesh/component/LightingWindow.h" namespace "echomesh":
  cdef cppclass LightingWindow:
    InstrumentGrid* grid()
    void saveSnapshotToFile(string)
    void setLights(FColorList)

  LightingWindow* makeLightingWindow() nogil
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

  def set_lights(self, ColorList lights):
    self.thisptr.setLights(lights.thisptr[0])

  def set_light_count(self, int count):
    self.thisptr.grid().setLightCount(count)

  def save_snapshot_to_file(self, object filename):
    self.thisptr.saveSnapshotToFile(filename)

  def set_shape(self, bool isRect):
    self.thisptr.grid().setShape(isRect)

  def set_show_label(self, bool show):
    self.thisptr.grid().setShowLabel(show)

  def set_label_starts_at_zero(self, bool at_zero):
    self.thisptr.grid().setShowLabel(at_zero)

  def set_layout(self, object layout, object size, object padding,
                 object instrument_padding, object label_padding):
    self.thisptr.grid().setLayout(layout, size, padding, instrument_padding,
                                  label_padding)

