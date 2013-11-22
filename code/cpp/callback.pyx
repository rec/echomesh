ctypedef void (*Callback)(void *user_data)

cdef void perform_callback(void* f):
  (<object>f)()

cdef void perform_callback_gil(void* f) with gil:
  (<object>f)()

