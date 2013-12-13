from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import DataFile
from echomesh.base import Yaml
from echomesh.base import Merge
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def config(_, scope, cfg):
  f = DataFile.config_file(scope)
  configs = Yaml.read(f) + [cfg]
  Yaml.write(f, Merge.merge(*configs))
  # TODO: needs to propagate!
  LOGGER.info('Changing configuration for %s', scope)

