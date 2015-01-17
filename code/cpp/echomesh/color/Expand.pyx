cdef extern from "echomesh/color/Expand.h" namespace "echomesh::color":
    FColorList expand(FColorList, int xMult, int yMult, int columns)

def expand_color_list(object fcl, int x_mult, int y_mult):
    cdef ColorList source
    cdef ColorList result

    source = toColorList(fcl)
    if not fcl.columns:
        return source

    result = ColorList(columns=fcl.columns * x_mult)
    result.thisptr.copy(expand(source.thisptr[0], x_mult, y_mult, fcl.columns))
    return result
