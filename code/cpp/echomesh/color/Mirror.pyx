cdef extern from "echomesh/color/Mirror.h" namespace "echomesh::color":
    FColorList mirror(FColorList, int x, int y, bool reverseX, bool reverseY)

def mirror_color_list(object fcl, unsigned int x, unsigned int y,
                      bool reverseX, bool reverseY):
    cdef ColorMatrix source
    cdef ColorMatrix result

    source = toColorMatrix(fcl)
    result = ColorMatrix()
    result.thisptr.copy(mirror(source.thisptr[0], x, y, reverseX, reverseY))
    return result
