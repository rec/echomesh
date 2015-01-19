cdef extern from "echomesh/color/Scroll.h" namespace "echomesh::color":
    FColorList scroll(FColorList, int dx, int dy, int columns, bool wrap)
    FColorList smoothScroll(FColorList, float dx, float dy, int columns, bool wrap,
                            CTransform* transform)

    FColorList smoothScroll(FColorList, float dx, float dy, int columns, bool wrap,
                            FloatFunction function)

def scroll_color_list(object fcl, float dx, float dy, int columns=0,
                      bool wrap=False, bool smooth=True,
                      string transform='identity'):
    cdef ColorList source
    cdef ColorList result
    cdef FloatFunction function

    source = toColorList(fcl)
    result = ColorList()
    columns = columns or source.columns
    if smooth:
        function = makeFunction(transform)
        result.thisptr.copy(
          smoothScroll(source.thisptr[0], dx, dy, columns, wrap, function))
    else:
        result.thisptr.copy(
          scroll(source.thisptr[0], int(dx), int(dy), columns, wrap))
    result.columns = columns
    return result
