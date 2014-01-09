cdef extern from "echomesh/color/FColor.h" namespace "echomesh::color":
  cdef cppclass FColor:
    FColor()
    FColor(unsigned int)
    FColor(float, float, float)
    FColor(float, float, float, float)

    float red()
    float green()
    float blue()
    float alpha()

    void combine(FColor x)
    bool compare(FColor)
    void copy(FColor)
    void copy(FColor*)
    void gamma(float)
    FColor interpolate(FColor end, float ratio)
    void scale(float)
