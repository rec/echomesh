include "echomesh/color/ColorList.pyx"

cdef class ColorMatrix(ColorList):
   pass

cdef ColorMatrix toColorMatrix(object value, columns=0):
    if isinstance(value, ColorMatrix):
        return <ColorMatrix> value
    return ColorMatrix(value, columns=columns)

def to_color_matrix(object x):
    return toColorMatrix(x)
