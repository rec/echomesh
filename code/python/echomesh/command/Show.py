from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Name
from echomesh.base import Path
from echomesh.base import Settings
from echomesh.base import Yaml
from echomesh.base.Join import join_words
from echomesh.command import Aliases
from echomesh.command import Contexts
from echomesh.command import Scores
from echomesh.expression import Transform
from echomesh.expression import Units
from echomesh.sound import Sound
from echomesh.util import Log
from echomesh.util.registry import Registry
import echomesh.command.Registry

LOGGER = Log.logger(__name__)

SHOW_REGISTRY = Registry.Registry('show command')
DEFAULT_INDENT = '    '

# TODO: remove in favor of _format.
def _indent(s, spaces=DEFAULT_INDENT):
    return '\n'.join(spaces + i.strip() for i in s.split('\n'))

def _format(info, spaces=DEFAULT_INDENT):
    s = Yaml.encode_one(info)
    LOGGER.info('\n' + DEFAULT_INDENT + s.replace('\n', '\n' + DEFAULT_INDENT))

def _info(d, spaces=DEFAULT_INDENT):
    s = 'none'
    if d:
        items = [(('%s%s:' % (spaces, k)), v)
                 for k, v in sorted(six.iteritems(d))]
        length = max(len(k) for k, v in items)
        s = '\n'.join('%-*s %s' % (length, k, ' '.join(v)) for k, v in items)
    LOGGER.info('%s\n', s)

def addresses(_):
    _info(Name.addresses())

def aliases(*_):
    al = Aliases.instance()
    if al:
        _info(al)
    else:
        LOGGER.info('    No aliases\n')

def _all(echomesh_instance):
    LOGGER.info('')
    for name in sorted(SHOW_REGISTRY.keys()):
        if name != 'all':
            LOGGER.info('%s:', name)
            SHOW_REGISTRY.function(name)(echomesh_instance)

def broadcast(echomesh_instance):
    message = 'ON' if echomesh_instance.broadcasting() else 'off'
    LOGGER.info('     Broadcast is %s\n', message)

def _settings(_, *names):
    settings = Settings.get_settings()
    names = set(names)
    keys = set(settings.keys())
    if 'all' in names:
        names = keys

    bad = names - set(settings.keys())
    if bad:
        LOGGER.error("Don't understand settings %s.", join_words(bad))
        names -= bad
    if names:
        _format(dict((k, v) for k, v in settings.items() if k in names))
    else:
        LOGGER.info('    Possible settings are:\n    ' +
                    join_words(settings.keys()))

def directories(_):
    _info(Path.info())

def elements(echomesh_instance):
    info = echomesh_instance.score_master.info()
    if info:
        _format(info)
    else:
        LOGGER.info('  No elements have been loaded into memory.\n')

def info(_):
    _info(Name.info())

def names(_):
    _info(Name.names())

def nodes(echomesh_instance):
    peers = echomesh_instance.peers.get_peers()
    if peers:
        for name, peer in six.iteritems(peers):
            LOGGER.info('  %s: ', name)
            _info(peer, '    ')
    else:
        LOGGER.error(NO_NODES_ERROR)

def sound(_):
    _info(Sound.info())

def timestamp(_):
    try:
        import cechomesh
        LOGGER.info('  cechomesh was built on %s, %s',
                    *cechomesh.build_timestamp())
    except:
        LOGGER.error('No cechomesh plugin found!')

def transforms(_):
    for k in sorted(Transform.REGISTRY.keys()):
        LOGGER.info('  %s\n%s\n', k,
                    _indent(Transform.REGISTRY.get_help(k), '    '))

def units(_):
    LOGGER.info('%s\n', Units.list_units())

def _variables(path, element, results):
    vars = getattr(element, 'variables', {})
    for k, v in six.iteritems(vars):
        results.append([path + [k], v()])
    for e in element.elements:
        _variables(path + [e.name], e, results)

def variables(instance):
    results = []
    for name, v in six.iteritems(instance.score_master.elements):
        _variables([name], v, results)

    if results:
        for path, value in sorted(results):
            LOGGER.info('  %s = %s', '.'.join(path), value)
        LOGGER.info('')
    else:
        LOGGER.info('  No variables have been set.\n')


NO_NODES_ERROR = """\
There are no echomesh nodes in your network.

Since there should always be at least the computer running echomesh, this
indicates a serious problem with your networking or your settings.

Consult the trouble-shooting guide for more information.
"""

ADDRESSES_HELP = """
Shows:
  This machine's current IP address.
  This machine's permanent MAC address.
"""

ALIASES_HELP = """
Shows all the command aliases that have been registered.
"""

BROADCAST_HELP = """
Shows if this echomesh node is in broadcast made, meaning that its run and pause
commands are sent to all other nodes.

When a node is in broadcast mode, the standard "echomesh:" prompt is replaced
by "echomesh!"

"""

SETTINGS_HELP = """
  "show settings" lists the merged settings values for all scopes.
  "show settings <scope> [<scope>...]" shows the separate settings
    for each scope.
  "show settings all" shows all the separate settings as well as the
    merged settings.
"""

NAMES_HELP = """
"show names" shows you the following information about this echomesh node:

  * The machine name (also called the uname for Linux machines).
  * The echomesh name.  This is by default the machine name but can be changed
    in the echomesh settings.
  * The echomesh tags for this machine, which are also set in the settings.
"""

INFO_HELP = """
"show info" shows your machine's info record.

Info is the list of identifying information sent from your machine to other
echomesh nodes - it is how you see remote nodes identified when you "show nodes"
and it's how your machine will be identified remotely.

info is made up of the "names" and "addresses" of this machine.

See "help show names" and "help show addresses" for more information.

"""

DIRECTORIES_HELP = """
"show path" shows directories that contain files used by echomesh:

  * The asset directory, where images, audio and other assets are stored.
  * The code directory, where the echomesh Python code is stored.
  * The command directory, which holds settings files and scores.
  * The project directory, the project root containing assets and commands.
  * The echomesh directory, which is the root of the echomesh installation.
"""

NODES_HELP = """
Each echomesh node knows about a list of other nodes on the same network.

"show nodes" lists "info" for each known node on the network, including itself.

See "help show info" for more information.
"""

ELEMENTS_HELP = """
"show elements" shows all the elements that have been loaded, as well as the
time they were started.

See "help start" and "help pause" for more information.
"""

SOUND_HELP = """
Show all the sound interfaces available on this machine.
"""

TIMESTAMP_HELP = """
Print the build date and time for the cechmesh plug-in.
"""

TRANSFORMS_HELP = """
Transforms are used to reshape curves.  Mathematically, they are invertible
mappings from [0, 1] onto [0, 1].

Whenever a transform is called for, you can name a single transform like

  sine

or you can compile a list of them, like

  sine.power.inverse.

"""

UNITS_HELP = """
echomesh understands data expressed in a variety of units like Hz, percent,
semitones and decibels.  "show units" lists these units and their synonyms
(like seconds, sec, s or second).

"""

VARIABLES_HELP = """
Show all variables for each element currently running.

"""

SHOW_REGISTRY.register_all(
    addresses=(addresses, ADDRESSES_HELP),
    aliases=(aliases, ALIASES_HELP),
    broadcast=(broadcast, BROADCAST_HELP),
    settings=(_settings, SETTINGS_HELP),
    contexts=(Contexts.contexts, Contexts.HELP),
    directories=(directories, DIRECTORIES_HELP),
    elements=(elements, ELEMENTS_HELP),
    info=(info, INFO_HELP),
    names=(names, NAMES_HELP),
    nodes=(nodes, NODES_HELP),
    scores=(Scores.scores, Scores.SCORES_HELP),
    sound=(sound, SOUND_HELP),
    timestamp=(timestamp, TIMESTAMP_HELP),
    transforms=(transforms, TRANSFORMS_HELP),
    units=(units, UNITS_HELP),
    variables=(variables, VARIABLES_HELP),
  )

SHOW_NAMES = SHOW_REGISTRY.join_keys()
SHOW_USAGE = 'You can show any of the following values: \n  %s.\n' % SHOW_NAMES

ALL_HELP = """
Shows all information on all values:
  %s
""" % SHOW_NAMES

SHOW_REGISTRY.register_all(all=(_all, ALL_HELP))

def _show(echomesh_instance, *parts):
    if not parts:
        LOGGER.info('\n' + SHOW_USAGE)
    else:
        name = parts[0]
        try:
            function = SHOW_REGISTRY.function(name)
        except:
            raise Exception("Didn't understand command 'show %s'. \n\n%s" %
                            (' '.join(parts), SHOW_USAGE))

        function(echomesh_instance, *parts[1:])

SHOW_HELP = """
"show" displays information about the current echomesh instance.

""" + SHOW_USAGE

echomesh.command.Registry.registry().register_all(show=(_show, SHOW_HELP))
