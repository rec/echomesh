from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Platform
from echomesh.util import Log
from echomesh.util import Subprocess

LOGGER = Log.logger(__name__)

OUTPUT_COMMAND = 'sudo', 'amixer', 'cset', 'numid=3'
COMMANDS = dict(default='0', audio='1', hdmi='2')
OUTPUT_SET = False

def set_output(output=None):
  output = output or Config.get('audio', 'output', 'route')
  if Platform.IS_LINUX:
    command = COMMANDS.get(output)
    if not command:
      LOGGER.error("Didn't understand output '%s'", output)
      return

    result, returncode = Subprocess.run(OUTPUT_COMMAND + (command, ))
    if returncode:
      LOGGER.error("Couldn't open output %s\n%s", output, result)
    else:
      LOGGER.debug('Set audio output to %s', output)
    global OUTPUT_SET
    OUTPUT_SET = True
