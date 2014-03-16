from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Platform

try:
  from RPi import GPIO
  GPIO.setmode(GPIO.BCM)

except ImportError:
  GPIO = None

RPI_ERROR = """RPi.GPIO is not installed on your Raspberry Pi.\n'
Please follow the instructions at
http://www.raspberrypi-spy.co.uk/2012/05/install-rpi-gpio-python-library/
"""

OTHER_ERROR = 'You can only listen to the GPIO pins on the Raspberry Pi.'

def on_gpio(callback, number, pull_up, bounce_time):
  if not GPIO:
    if Platform.PLATFORM == Platform.RASPBERRY_PI:
      raise Exception(RPI_ERROR)
    else:
      raise Exception(OTHER_ERROR)

  pull_up_down = GPIO.PUD_UP if pull_up else GPIO.PUD_DOWN
  GPIO.setup(number, GPIO.IN, pull_up_down=pull_up_down)
  GPIO.add_event_detect(number, GPIO.RISING, callback=callback,
                        bouncetime = bounce_time)

