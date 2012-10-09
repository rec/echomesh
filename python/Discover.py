#!/usr/bin/python

from network import Discovery
from config import Config

if __name__ == '__main__':
  discovery = Discovery.Discovery(Config.discovery_port)
  discovery.thread.join()
