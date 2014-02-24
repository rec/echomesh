cdef extern from "echomesh/color/Scroll.h" namespace "echomesh::color":
  FColorList scroll(FColorList, int dx, int dy, int xSize, bool wrap)

def scroll_color_list(object fcl, int dx, int dy, int x_size, bool wrap):
  cdef ColorList source
  cdef ColorList result

  source = toColorList(fcl)
  result = ColorList()
  result.thisptr.copy(scroll(source.thisptr[0], dx, dy, x_size, wrap))
  return result
