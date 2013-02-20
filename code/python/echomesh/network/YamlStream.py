from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

from echomesh.util.thread import RunnableQueue


def queue_source(queue, runnable, timeout):
  while runnable.is_running:
    try:
      yield queue.get(timeout)
    except queue.Empty:
      pass

def queue_sink(generator, queue, runnable):
  for g in generator:
    if runnable.is_running:
      queue.put(g)
    else:
      return

for packet in yaml.safe_load_all(queue_source(input_queue, runnable, timeout)):
  pass



yaml.safe_dump_all(queue_source(output_queue, runnable, timeout), socket_output_queue)



    self.queue = queue.Queue()

  def queue_iterator(self):
    while self.is_running:
      try:
        yield self.queue.get(timeout=DEFAULT_TIMEOUT)
      except queue.Empty:
        pass
    setattr(self.socket, 'echomesh_socket', self)


class YamlReceiveSocket(ThreadRunnable):
  def __init__(self):
    self.queue = queue.Queue()

  def target(self):
    for item in queue_source(self.queue, self):



def pad(iter, stopper=None):
  for i in iter:
    if stopper and not stopper.is_running:
      return
    yield i
    yield None

def unpad(item, stopper=None):
  for i in iter:
    if stopper and not stopper.is_running:
      return
    if i is not None:
      yield i


def read_generator(input):
  return unpad(yaml.safe_load_all(input))

def write_from_generator(generator, output):
  yaml.safe_dump_all(pad(generator), output)

"""

Threads:

  1. A select thread that polls all the readers and writers.
  2. A read thread that pulls YAML off a queue and then directs it to the remote
  receive.
  3.


"""



from six.moves import queue

from echomesh.util.thread import Runnable

DEFAULT_TIMEOUT = 0.5

class RunnableQueue(Runnable.Runnable):
  def __init__(self):
    super(RunnableQueue, self).__init__()
    self.queue = queue.Queue()

  def get(self):
    return


class QueueWriter(ThreadLoop):
  def __init__(self, output):
    super(QueueWriter, self).__init__()
    self.queue = queue.Queue()
    self.output = output

  def single_loop(self):
    try:
      item = self.queue.get(timeout=DEFAULT_TIMEOUT)
    except queue.Empty:
      pass
    else:
      item and output(item)



class QueueReader(ThreadLoop):
  def __init__(self, input):
    super(QueueReader, self).__init__()
    self.queue = queue.Queue()

  def single_loop(self):
    try:
      item = self.queue.get(timeout=DEFAULT_TIMEOUT)
    except queue.Empty:
      pass
    else:

    if item is not None:


class QueueWriter(ThreadLoop):
  def __init__(self, input):
    super(QueueWriter, self).__init__()
    self.queue = queue.Queue()

  def single_loop(self):
    try:
      data = self.queue.get(timeout=DEFAULT_TIMEOUT)
    except queue.Empty:
      pass
    else:
      stream.write(data)



def stream_to_yml(generator_returning_strings):
  return yaml.safe_dump_all(generator_returning_strings)


def generator_from_socket

