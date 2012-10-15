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
  card: "sysdefault:CARD=AK5370",
  periodsize: 160,
  levels: [-25, -15, -5]
}
"""

LOCAL_FILE = '~/.echomesh'
LOCAL_CHANGED_FILE = '~/.echomesh-changed'

CODE_CONFIG = yaml.safe_load(CODE_CONFIG_STRING)
LOCAL_CONFIG = File.yaml_load(LOCAL_FILE)
CHANGED_CONFIG = File.yaml_load(LOCAL_CHANGED_FILE)

def config():
  return Merge.merge_all(CODE_CONFIG, LOCAL_CONFIG, CHANGED_CONFIG)

def change(config):
  global CHANGED_CONFIG
  CHANGED_CONFIG = config
  File.write_yaml(LOCAL_CHANGED_FILE, CHANGED_CONFIG)
