cdef extern from "echomesh/color/HSB.h" namespace "echomesh::color::HSB":
    float interpolateHue(float x, float y, float r)
    FColor hsbFromRgb(FColor color)

def interpolate_hue(float x, float y, float r):
    return interpolateHue(x, y, r)
