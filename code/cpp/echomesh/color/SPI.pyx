cdef extern from "echomesh/color/SPI.h" namespace "echomesh::color":
  enum Order:
    pass
  Order getOrder(string)
  void fillSpi(FColorList, char*, int length, Order order)

def get_spi_order(string s):
  cdef Order o
  o = getOrder(s)
  if o < 0:
    raise Exception('Don\'t understand SPI order %s.' % s)
  return o

def fill_spi(ColorList cl, bytearray b, Order order):
  cdef char* bptr = PyByteArray_AsString(b)
  fillSpi(cl.thisptr[0], bptr, len(b), order)

def combine_to_spi(list data, float brightness, float gamma, bytearray b,
                   Order order):
  cdef ColorList cl = combine_color_lists(data)
  cl.scale(brightness)
  cl.gamma(gamma)
  fill_spi(cl, b, order)
