from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing

from command import Router
from config import Config
from network import Discovery
from sound import Microphone

if __name__ == '__main__':
  discovery = Discovery.Discovery(Config.discovery_port,
                                  Config.discovery_timeout,
                                  Router.ROUTER)
  mic = Microphone.run_mic_levels_thread(print, Config)
  with closing(discovery):
    with closing(mic):
      raw_input('Press return to exit\n')

  discovery.join()
