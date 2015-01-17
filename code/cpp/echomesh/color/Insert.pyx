cdef extern from "echomesh/color/Insert.h" namespace "echomesh::color":
    FColorList insert(FColorList fcl,
                      int offset, unsigned int length, bool rollover, int skip)

def insert_color_list(object fcl,
                      int offset, unsigned int length, bool rollover, int skip):
    cdef ColorMatrix source
    cdef ColorMatrix result

    source = toColorMatrix(fcl)
    result = ColorMatrix()
    result.thisptr.copy(insert(source.thisptr[0], offset, length, rollover, skip))
    return result
