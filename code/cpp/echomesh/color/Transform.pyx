cdef extern from "echomesh/color/Transform.h" namespace "echomesh::color":
    cdef cppclass CTransform:
        float apply(float x)
        float inverse(float x)

    cdef CTransform* makeTransform(string)

    cdef cppclass FloatFunction:
        pass

    cdef float apply(FloatFunction, float)
    cdef bool empty(FloatFunction)
    cdef FloatFunction makeFunction(string)

cdef class Transform:
    cdef CTransform* thisptr

    def __cinit__(self, object s):
        if not isinstance(s, six.string_types):
            raise ValueError('Transform description "%s" is not a string' % s)

        self.thisptr = makeTransform(s)
        if not self.thisptr:
            raise ValueError('Couldn\'t understand transform %s' % s)

    def __dealloc__(self):
        del self.thisptr

    def apply(self, float x):
        return self.thisptr.apply(x)

    def inverse(self, float x):
        return self.thisptr.inverse(x)

cdef class Function:
    cdef FloatFunction function
    cdef string desc

    def __cinit__(self, object desc):
        if not isinstance(desc, six.string_types):
            raise ValueError('FloatFunction desc "%s" is not a string' % desc)

        self.function = makeFunction(desc)
        self.desc = desc

    property desc:
        def __get__(self):
            return self.desc

    def __str__(self):
        return self.desc

    def __call__(self, float x):
        if not self:
            raise ValueError('Empty function %s' % self)
        return apply(self.function, x)

    def __nonzero__(self):
        return not empty(self.function)
