from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

FAKE = not True
DEBUG = FAKE or not True
SUSPICIOUS_LOCK = -1

class _Locker(object):
    INDEX = 0

    def __init__(self, lock):
        self.lock = lock
        self.index = _Locker.INDEX
        _Locker.INDEX += 1
        print('--- Creating lock %d ---' % self.index)
        self.tb()

    def __enter__(self):
        print('entering lock', self.index)
        self.tb()
        self.lock.__enter__()
        print('entered lock', self.index)

    def tb(self):
        if self.index == SUSPICIOUS_LOCK:
            for line in traceback.format_stack():
                print(line.strip())

    def __exit__(self, exc_type, exc_value, traceback):
        print('exiting lock', self.index)
        self.lock.__exit__(exc_type, exc_value, traceback)
        print('exited lock', self.index)

class _FakeLock(object):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def Lock(fake=False):
    if fake:
        return _FakeLock()
    lock = threading.RLock()
    return _Locker(lock) if DEBUG else lock

def RLock(fake=False):
    if fake:
        return _FakeLock()
    lock = threading.RLock()
    return _Locker(lock) if DEBUG else lock
