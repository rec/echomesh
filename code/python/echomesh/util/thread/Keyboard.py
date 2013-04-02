from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import time

from echomesh.base import Config
from echomesh.command import Command
from echomesh.expression import Units
from echomesh.util import Log
from echomesh.util.thread import ThreadRunnable

LOGGER = Log.logger(__name__)

MESSAGE = """Type help for a list of commands.
"""

class Keyboard(ThreadRunnable.ThreadRunnable):
  def __init__(self, sleep, message, processor,
               prompt='echomesh', output=sys.stdout):
    super(Keyboard, self).__init__(name='Keyboard')
    self.sleep = sleep
    self.message = message
    self.processor = processor
    self.prompt = prompt
    self.output = output
    self.alert_mode = False

  def target(self):
    self._begin()
    while self.is_running:
      self._input_loop()

  def _begin(self):
    self.output.write('\n')
    self.output.flush()
    if self.sleep:
      time.sleep(self.sleep)
      self.sleep = 0
    if self.message:
      print(self.message)
      self.message = ''

  def _input_loop(self):
    buff = ''
    first_time = True
    brackets, braces = 0, 0
    while first_time or brackets > 0 or braces > 0:
      # Keep accepting new lines as long as we have a surplus of open
      # brackets or braces.
      if first_time:
        first_time = False
        self.output.write(self.prompt)
      else:
        self.output.write(' ' * len(self.prompt))
      self.output.write('!' if self.alert_mode else ':')
      self.output.write(' ')
      self.output.flush()

      data = raw_input()
      buff += data

      brackets += (data.count('[') - data.count(']'))
      braces += (data.count('{') - data.count('}'))

    if brackets < 0:
      LOGGER.error('Too many ]')
    elif braces < 0:
      LOGGER.error('Too many }')
    elif self.processor(buff.strip()):
      self.pause()


USE_CURSES = Config.get('control_program', 'use_curses')

if USE_CURSES:

  # pylint: disable=E0202,E1101,C0322,W0232,W0612,

  import npyscreen

  class RunnableApp(ThreadRunnable.ThreadRunnable):
    def __init__(self):
      super(RunnableApp, self).__init__()
      self.app = TestApp()

    def target(self):
      self.app.run()

  class TestApp(npyscreen.NPSApp):
    def main(self):
      # These lines create the form and populate it with widgets.
      # A fairly complex screen in only 8 or so lines of code - a line for each control.
      self.keypress_timeout_default = 10
      F = npyscreen.ActionForm(parentApp=self, name="Welcome to Npyscreen",)
      t = F.add(npyscreen.TitleText, name="Text:", )
      fn = F.add(npyscreen.TitleFilename, name="Filename:")
      dt = F.add(npyscreen.TitleDateCombo, name="Date:")
      s = F.add(npyscreen.TitleSlider, out_of=12, name="Slider", color='DANGER')
      ml= F.add(npyscreen.MultiLineEdit,
                value = """try typing here!\nMutiline text, press ^R to reformat.\n""",
        max_height=5, rely=9)
      ms= F.add(npyscreen.TitleSelectOne, max_height=4, value=[1], name="Pick One",
                values = ["Option1","Option2","Option3"], scroll_exit=True)

      # This lets the user play with the Form.
      F.edit()

  def keyboard(_):
    return RunnableApp()

else:
  def keyboard(echomesh):
    processor = lambda line: Command.execute(echomesh, line)
    sleep = Units.get_config('delay_before_keyboard_activates')
    return Keyboard(sleep=sleep, message=MESSAGE, processor=processor)
