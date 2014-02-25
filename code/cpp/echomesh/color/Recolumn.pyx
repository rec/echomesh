cdef extern from "echomesh/color/Recolumn.h" namespace "echomesh::color":
  void recolumn(FColorList*, int oldColumns, int newColumns)
  bool mustRecolumn(int oldColumns, int newColumns)

