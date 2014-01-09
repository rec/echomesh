cdef extern from "echomesh/color/SPI.h" namespace "echomesh::color":
  enum Order:
    pass
  Order getOrder(string)
  void fillSpi(FColorList, unsigned char*, order)

def get_spi_order(string s):
  cdef Order o
  o = getOrder(s)
  if o < 0:
    raise Exception('Don\'t understand SPI order %s.' % s)
  return o
