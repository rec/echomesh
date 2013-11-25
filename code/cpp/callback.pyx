from libcpp.string cimport string

ctypedef void (*Callback)(void *user_data)
ctypedef void (*StringCallback)(void *user_data, string)

cdef void perform_callback(void* f):
  (<object>f)()

cdef void perform_callback_gil(void* f) with gil:
  (<object>f)()

cdef void perform_string_callback_gil(void* f, string s) with gil:
  (<object>f)(s)

