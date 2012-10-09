#!/usr/bin/python

from contextlib import closing

from network import Discovery
from config import Config

if __name__ == '__main__':
  discovery = Discovery.Discovery(Config.discovery_port,
                                  Config.discovery_timeout)
  with closing(discovery):
    raw_input('Press return to exit\n')
  discovery.thread.join()
