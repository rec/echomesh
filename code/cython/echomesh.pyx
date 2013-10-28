# distutils: language = c++
# distutils: sources = Tiny.cpp

cdef extern from "Tiny.h" namespace "echomesh":
    cdef cppclass Foo:
        void bar()


cdef class PyFoo:
    cdef Foo *thisptr

    def __cinit__(self):
        self.thisptr = new Foo()

    def bar(self):
        self.thisptr.bar()