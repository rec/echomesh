from __future__ import absolute_import, division, print_function, unicode_literals

from util import Subprocess

if __name__ == '__main__':
  for line in Subprocess.run(['sudo', 'ls', '/root']).splitlines():
    print(line)
