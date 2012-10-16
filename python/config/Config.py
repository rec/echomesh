from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import sys
import yaml

from util import File
from util import Merge

CODE_CONFIG_STRING = """
type: config

include_url: true
use_shortener: true
shorten_url: http://ax.to
shorten_prefix: e
index_file: /home/tom/shortenIndex.txt
use_index_url: true

git_user: rec
git_project: echomesh
discovery_port: 1238
discovery_timeout: 0.100
allow_shutdown: true

mic: {
  samplerate: 8000,
  name: AK5370,
  periodsize: 160,
  levels: [-25, -15, -5]
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
