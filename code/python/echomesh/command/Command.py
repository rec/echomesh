from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Aliases
from echomesh.base import Join

# pylint: disable=W0611
from echomesh.command import Alias, Broadcast, ElementCommands, GetConfig
from echomesh.command import CommandRegistry, RemoteCommands, SaveConfig, SetConfig
from echomesh.command import Show, TransferCommand

# Must be the last one to load.
from echomesh.command import Help

# pylint: enable=W0611
# TODO: use the late loading from echomesh.element

from echomesh.util import FindComment
from echomesh.util import Log
from echomesh.util import Split

LOGGER = Log.logger(__name__)

COMMENT_HELP = """
Comment lines start with a # - everything after that is ignored.
"""

CommandRegistry.register(lambda e: None, '#', COMMENT_HELP)
CommandRegistry.register(None, 'sample', 'This is a sample with just help')

def _fix_exception_message(m, name):
  loc = m.find(')')
  if loc >= 0:
    m = m[loc + 1:]
  m = (m.replace('1', '0').
       replace('2', '1').
       replace('3', '2').
       replace('4', '3').
       replace('1 arguments', '1 argument'))
  return name + m

def usage():
  result = ['Valid commands are:', CommandRegistry.join_keys()]
  aliases = Aliases.instance()
  if aliases:
    result.append('\nand aliases are:')
    result.append(Join.join_words(aliases))
  return ' '.join(result)

def _expand(command):
  aliases = Aliases.instance()
  stack = set()
  result = []

  def expand(*cmds):
    for command in cmds:
      parts = Split.split_words(command)
      name = parts.pop(0)
      alias = aliases.get_prefix(command)
      if alias:
        cmd, alias_commands = alias
        registry = CommandRegistry.get_or_none(name)
        if cmd == command or (not registry or registry[0] != name):
          assert cmd not in stack
          stack.add(cmd)
          expand(*alias_commands)
          stack.remove(cmd)
          continue

      result.append([CommandRegistry.get(name), parts])
  expand(command)
  return result

def execute(instance, line):
  line = FindComment.remove_comment(line).strip()
  if not line:
    LOGGER.info('')
    return

  try:
    commands = _expand(line)
  except TypeError as e:
    e.message = _fix_exception_message(e.message, line)
    LOGGER.error()
    return
  except:
    LOGGER.error("Didn't understand command %s\n%s" % (line, usage()),
                 exc_info=False)
    return

  for function, parts in commands:
    try:
      function(instance, *parts)
    except:
      LOGGER.error()
