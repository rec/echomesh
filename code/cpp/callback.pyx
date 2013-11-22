ctypedef void (*Callback)(void *user_data)

cdef void perform_callback(void* f):
  (<object>f)()

