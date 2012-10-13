from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing

from command import Router
from config import Config
from network import Discovery
from util import Platform

if __name__ == '__main__':
  discovery = Discovery.Discovery(Config.discovery_port,
                                  Config.discovery_timeout,
                                  Router.ROUTER)
  if Platform.IS_LINUX:
    mic = Microphone.run_mic_levels_thread(print, Config)

  with closing(discovery):
    raw_input('Press return to exit\n')

  if Platform.IS_LINUX:
    mic.close()

  discovery.join()
