import cechomesh
import time

loudness = cechomesh.AudioLoudness('AK5370', 1)
loudness2 = cechomesh.AudioLoudness('AK5370', 1)

print('deleting first')
loudness = None
print('deleting second')
loudness2 = None
