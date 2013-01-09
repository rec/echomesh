from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util import Platform
from echomesh.util import Subprocess

LOGGER = Log.logger(__name__)

OUTPUT_COMMAND = 'sudo', 'amixer', 'cset', 'numid=3'
COMMANDS = dict(default='0', audio='1', hdmi='2')

def set_output(output):
  if Platform.IS_LINUX:
    command = COMMANDS.get(output, None)
    if not command:
      LOGGER.error("Didn't understand output '%s'", output)
      return

    result, returncode = Subprocess.run(OUTPUT_COMMAND + (command, ))
    if returncode:
      LOGGER.error("Couldn't open output %s\n%s", output, result)
    else:
      LOGGER.info('Set audio output to %s', output)
