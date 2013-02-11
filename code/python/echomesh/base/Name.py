# from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import os
import platform
import socket

from contextlib import closing

from echomesh.base import Platform

def ip_address():
  try:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
      s.connect(('8.8.8.8', 80))
      return s.getsockname()[0]
  except:
    return '(none)'

if Platform.IS_LINUX:
  import fcntl, socket, struct

  # From here: http://stackoverflow.com/questions/159137/getting-mac-address
  def get_hw_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # b = b'256s'
    b = '256s'
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack(b, ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

  def mac_address():
    return get_hw_addr('eth0')

else:
  import uuid
  def mac_address():
    myMAC = uuid.getnode()
    return ':'.join('%02X' % ((myMAC >> 8*i) & 0xff) for i in reversed(xrange(6)))

MAC_ADDRESS = mac_address()
IP_ADDRESS = ip_address()
UNAME = platform.uname()[1]

NAME = UNAME
def set_name(name):
  global NAME
  NAME = name

def lookup(table, default=None):
  """
  Look up the machine's name in a table, first by MAC address,
  then by IP address and finally by uname.
  """
  none = object()
  for name in MAC_ADDRESS, IP_ADDRESS, UNAME, NAME:
    value = table.get(name, none)
    if value is not none:
      return value
  return default
