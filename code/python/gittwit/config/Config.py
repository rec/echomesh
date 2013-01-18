from __future__ import absolute_import, division, print_function, unicode_literals

CONFIG = dict(
  git=dict(
    project='git-twit',
    user='rec',
  ),

  logging=dict(
    #  file='~/log/git-twit.log',
    level='info',
    ),

  shorten=dict(
    enable=True,
    include_url=True,
    index_file='/home/tom/shortenIndex.txt',
    prefix='e',
    url='http://ax.to',
    use_index_url=True,
    ),
)
