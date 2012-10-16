from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import sys
import yaml

from util import File
from util import Merge

# Universal configuration.
CONFIG_STRING = """

type: config

allow_shutdown: true

discovery: {
  port: 1238,
  timeout: 0.100
}

git: {
  user: rec,
  project: echomesh,
}

mic: {
  samplerate: 8000,
  name: AK5370,
  periodsize: 160,
  levels: [-25, -15, -5],
}

shorten: {
  enable: true,
  include_url: true,
  index_file: /home/tom/shortenIndex.txt,
  prefix: e,
  url: "http://ax.to",
  use_index_url: true,
}
"""

# Configurations per nodename.
NODENAME_CONFIG_STRING = """
"""

# Local configuration for this account.
LOCAL_FILE = '~/.echomesh'

# Stores the last dynamic configuration update.
LOCAL_CHANGED_FILE = '~/.echomesh-changed'

STORE_LOCAL_CHANGED_FILE = True

CONFIG = Merge.merge_into_all(
  yaml.safe_load(CONFIG_STRING),
  yaml.safe_load(NODENAME_CONFIG_STRING).get(Address.NODENAME, {}),
  File.yaml_load(LOCAL_FILE, False),
  File.yaml_load(LOCAL_CHANGED_FILE, False))

if len(sys.argv) > 1:
  print('Merging config from file', sys.argv[1])
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1].strip()))

def change(config):
  File.write_yaml(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))

# TODO: a "clear" command that undoes the "change" command.  A tiny bit tricky,
# because we'd have to revert the main config to its original value "in place".
