# Dead simple log for debugging unit tests, where outputing to stdio makes tests
# break.

LOG_FILE = '/tmp/log.txt'

with open(LOG_FILE, 'w') as f:
  pass

def LOG(*args):
  with open(LOG_FILE, 'a') as f:
    for a in args:
      f.write(str(a))
      f.write(', ')
    f.write('\n')

