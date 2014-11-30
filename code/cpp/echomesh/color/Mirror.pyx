cdef extern from "echomesh/color/Mirror.h" namespace "echomesh::color":
    FColorList mirror(FColorList, int x, int y, bool reverseX, bool reverseY)

def mirror_color_list(object fcl, unsigned int x, unsigned int y,
                      bool reverseX, bool reverseY):
    cdef ColorList source
    cdef ColorList result

    source = toColorList(fcl)
    result = ColorList()
    result.thisptr.copy(mirror(source.thisptr[0], x, y, reverseX, reverseY))
    return result
