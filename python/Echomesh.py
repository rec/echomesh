from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing

from command import Router
from config import Config
from network import Discovery
from util import Platform

ENABLE_MIC = True

if __name__ == '__main__':
  discovery = Discovery.Discovery(Config.CONFIG['discovery_port'],
                                  Config.CONFIG['discovery_timeout'],
                                  Router.ROUTER)
  with closing(discovery):
    use_mic = ENABLE_MIC and Platform.IS_LINUX
    if use_mic:
      from sound import Microphone
      mic = Microphone.run_mic_levels_thread(print, Config.CONFIG)

    raw_input('Press return to exit\n')

    if use_mic:
      mic.close()

  discovery.join()
