CONFIG=dict(
  include_url = True,
  use_shortener = True,
  shorten_url = 'http://ax.to',
  shorten_prefix = 'e',
  index_file = '/home/tom/shortenIndex.txt',
  use_index_url = True,

  git_user = 'rec',
  git_project = 'echomesh',
  discovery_port = 1238,
  discovery_timeout = 0.100,
  allow_shutdown = True,

  mic = dict(samplerate=8000,
             card='sysdefault:CARD=AK5370',
             periodsize=160,
             levels=[-25, -15, -5])
)
