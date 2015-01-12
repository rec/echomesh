cdef enum Centering:
  BEGIN = -1
  MIDDLE = 0
  END = 1

cdef extern from "echomesh/color/Tile.h" namespace "echomesh::color":
    FColorList tile(FColorList, int xMult, int yMult, int columns)
    FColorList tile_pieces(FColorList, int columns, int newColumns, int newRows,
        int xCenter, int yCenter)

def tile_color_list(object fcl, int x_mult, int y_mult):
    cdef ColorList source
    cdef ColorList result

    source = toColorList(fcl)
    if not fcl.columns:
        return source

    result = ColorList(columns=fcl.columns * x_mult)
    result.thisptr.copy(tile(source.thisptr[0], x_mult, y_mult, fcl.columns))
    return result

def tile_colors(object fcl, int new_columns, int new_rows,
                int x_center=-1, int y_center=-1):

    cdef ColorList source
    cdef ColorList result

    source = toColorList(fcl)
    old_columns = fcl.columns or len(fcl)
    if not old_columns:
        return source

    result = ColorList(columns=new_columns)
    result.thisptr.copy(tile_pieces(
        source.thisptr[0], old_columns,
        new_columns, new_rows, x_center, y_center))
    return result

#
