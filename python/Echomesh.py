#!/usr/bin/python

from contextlib import closing

from command import Router
from config import Config
from network import Discovery

if __name__ == '__main__':
  discovery = Discovery.Discovery(Config.discovery_port,
                                  Config.discovery_timeout,
                                  Router.ROUTER)
  with closing(discovery):
    raw_input('Press return to exit\n')

  discovery.send_thread.join()
  discovery.receive_thread.join()
