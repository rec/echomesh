cdef extern from "echomesh/color/Tile.h" namespace "echomesh::color":
  FColorList tile(FColorList, int xMult, int yMult, int columns)

def tile_color_list(object fcl, int x_mult, int y_mult, int columns=0):
  cdef ColorList source
  cdef ColorList result

  source = toColorList(fcl)
  columns = columns or fcl.columns
  if not columns:
    return source

  result = ColorList(columns=columns * x_mult)
  result.thisptr.copy(tile(source.thisptr[0], x_mult, y_mult, columns))
  return result
