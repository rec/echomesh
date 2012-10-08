#!/usr/bin/python

# From here: http://stackoverflow.com/questions/159137/getting-mac-address

import Platform

if Platform.IS_LINUX:
  import fcntl, socket, struct

  def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

  def MacAddress():
    return getHwAddr('eth0')

else:
  import uuid

  # See http://stackoverflow.com/questions/12404622/python-get-normal-hex-format-for-mac-adress
  def MacAddress():
    myMAC = uuid.getnode()
    return ':'.join('%02X' % ((myMAC >> 8*i) & 0xff) for i in reversed(xrange(6)))

if __name__ == '__main__':
  print MacAddress()
