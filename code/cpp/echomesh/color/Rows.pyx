cdef extern from "echomesh/color/Rows.h" namespace "echomesh::color":
    int computeRows(int size, int columns)

def compute_rows(int size, int columns):
    return computeRows(size, columns)
