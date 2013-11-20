from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import time

from echomesh.base import Config
from echomesh.command import Command
from echomesh.expression import Expression
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.thread.ThreadRunnable import ThreadRunnable
import npyscreen, curses

LOGGER = Log.logger(__name__)

MESSAGE = """Type help for a list of commands.
"""
USE_CURSES = Config.get('control_program', 'use_curses')

class Keyboard(MasterRunnable):
  def __init__(self, sleep, message, processor,
               prompt='echomesh', output=sys.stdout):
    super(Keyboard, self).__init__()
    self.sleep = sleep
    self.message = message
    self.processor = processor
    self.prompt = prompt
    self.output = output
    self.alert_mode = False

  def loop(self):
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

      data = sys.stdin.readline()
      buff += data

      brackets += (data.count('[') - data.count(']'))
      braces += (data.count('{') - data.count('}'))

    if brackets < 0:
      LOGGER.error('Too many ]')
    elif braces < 0:
      LOGGER.error('Too many }')
    elif self.processor(buff.strip()):
      self.pause()

if USE_CURSES:
  def keyboard(instand, new_thread=True):
    return TestApp().run()

else:

  def keyboard(instance, new_thread=True):
    def processor(line):
      try:
        return Command.execute(instance, line)
      except:
        LOGGER.error('Error processing command line.')

    sleep = Expression.convert(Config.get('delay_before_keyboard_activates'))
    keyboard = Keyboard(sleep=sleep, message=MESSAGE, processor=processor)
    if new_thread:
      runnable = ThreadRunnable(target=keyboard.loop)
      runnable.add_mutual_pause_slave(keyboard)
      return runnable

    return keyboard

class TestApp(npyscreen.NPSAppManaged):
  def onStart(self):
    self.addForm("MAIN", MainForm, name='Welcome to Echomesh!')

class MainForm(npyscreen.ActionFormWithMenus):
  def create(self):
    self.add(npyscreen.TitleText, name="Text:", value="Click cancel to quit application")

     # The menus are created here.
    self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
    self.m1.addItemsFromList([
        ("Just Beep",   self.whenJustBeep, "e"),
        ("Exit Application", self.exit_application, "X"),
    ])

    self.m2 = self.add_menu(name="Another Menu", shortcut="b")
    self.m2.addItemsFromList([
        ("Just Beep",   self.whenJustBeep),
    ])

    self.m3 = self.m2.addNewSubmenu("A sub menu", "^F")
    self.m3.addItemsFromList([
        ("Just Beep",   self.whenJustBeep),
    ])

  def whenJustBeep(self):
    curses.beep()

  def exit_application(self):
    curses.beep()
    sys.exit(0)

  def on_ok(self):
    self.exit_application()

  def on_cancel(self):
    self.exit_application()