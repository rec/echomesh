from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import sys
import yaml

from util import File
from util import Merge

CODE_CONFIG_STRING = """

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
  url: http://ax.to,
  use_index_url: true,
}
"""

LOCAL_FILE = '~/.echomesh'
LOCAL_CHANGED_FILE = '~/.echomesh-changed'

CODE_CONFIG = yaml.safe_load(CODE_CONFIG_STRING)
LOCAL_CONFIG = File.yaml_load(LOCAL_FILE)
CHANGED_CONFIG = File.yaml_load(LOCAL_CHANGED_FILE)
CONFIG = Merge.merge_into_all(copy.deepcopy(CODE_CONFIG), LOCAL_CONFIG,
                              CHANGED_CONFIG)

if len(sys.argv) > 1:
  print('Merging config from file', sys.argv[1])
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1].strip()))

def change(config):
  File.write_yaml(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))
