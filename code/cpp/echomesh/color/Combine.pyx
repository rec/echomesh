cdef extern from "echomesh/color/Combine.h" namespace "echomesh::color":
    ctypedef enum Combiner:
        NONE, ADD, SUBTRACT, MULTIPLY, DIVIDE, MIN, MAX, AND, OR, XOR

    ctypedef vector[FColorList*] FColorListList
    Combiner makeCombiner(string)
    string combinerNames()
    ctypedef void (*CombinerFunction)(FColor, FColor)
    CombinerFunction getCombinerFunction(string)
    FColorList combine(FColorListList , CombinerFunction)

cdef class CombinerPy:
    cdef CombinerFunction combiner

    def __cinit__(self, string name='max'):
        self.combiner = getCombinerFunction(name)
        if not self.combiner:
            raise ValueError('Don\'t understand combiner "%s".' % name)

    def combine(self, object patterns):
        cdef FColorListList fpats
        pats = [toColorList(p) for p in patterns]
        for p in pats:
            fpats.push_back((<ColorList> p).thisptr)

#
