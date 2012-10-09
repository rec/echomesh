#!/usr/bin/python

from network import Discovery
from config import Config

if __name__ == '__main__':
  discovery = Discovery.Discovery(Config.discovery_port,
                                  Config.discovery_timeout)
  input('Press return to exit')
  discovery.stop()
  discovery.thread.join()
