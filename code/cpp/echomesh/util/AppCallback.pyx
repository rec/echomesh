import traceback

from libcpp.string cimport string

ctypedef void (*VoidCaller)(void *user_data)
ctypedef void (*StringCaller)(void *user_data, string)

cdef void perform_callback(void* f) with gil:
    (<object>f)()

cdef void perform_string_callback(void* f, string s) with gil:
    try:
        (<object>f)(s)
    except:
        traceback.print_exc(limit=100)
