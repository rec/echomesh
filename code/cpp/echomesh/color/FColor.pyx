cdef extern from "echomesh/color/Colors.h" namespace "echomesh::color":
  cdef cppclass FColor:
    FColor()
    FColor(unsigned int)
    FColor(float, float, float)
    FColor(float, float, float, float)

    float alpha()
    float* parts()
    bool compare(FColor)
    void copy(FColor)
    void copy(FColor*)