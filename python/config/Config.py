from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import sys
import yaml

from network import Address
from util import File
from util import Merge

# Universal configuration.
CONFIG_STRING = """

type: config

allow_shutdown: true
control_program: true

discovery:
  port: 1238
  timeout: 0.10

display:
  dimensions: [0, 0, 400, 400]
  frames_per_second: 30
  full_screen: true
  library: pi3d

git:
  user: rec
  project: echomesh

logging:
#  file: ~/log/echomesh.log  # Uncomment to create a file
  level: debug

audio:
  library: pyaudio
  input:
#    enable: false
    samplerate: 8000
    name: AK5370
    periodsize: 160
    levels:
      silent: -60
      quiet: -55
      moderate: -50
      medium: -45
      loud: 0

shorten:
  enable: true
  include_url: true
  index_file: /home/tom/shortenIndex.txt
  prefix: e
  url: "http://ax.to"
  use_index_url: true

"""

# Configurations per nodename.
NODENAME_CONFIG_STRING = """
hofmann:
  display:
    enable: false

  audio:
    input:
      use_default: true

  control_program: true
"""

# Local configuration for this account.
LOCAL_FILE = '~/.echomesh'

# Stores the last dynamic configuration update.
LOCAL_CHANGED_FILE = '~/.echomesh-changed'

STORE_LOCAL_CHANGED_FILE = True

CONFIG = Merge.merge_into_all(
  yaml.safe_load(CONFIG_STRING),
  yaml.safe_load(NODENAME_CONFIG_STRING.strip()).get(Address.NODENAME, {}),
  File.yaml_load(LOCAL_FILE),
  File.yaml_load(LOCAL_CHANGED_FILE))

if len(sys.argv) > 1:
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1].strip()))

def change(config):
  File.write_yaml(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))

# TODO: a "clear" command that undoes the "change" command.  A tiny bit tricky,
# because we'd have to revert the main config to its original value "in place".
