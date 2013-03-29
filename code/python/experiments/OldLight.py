from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

def combine_lights(table, combiner, index, value):
  old = table.get(index)
  table[index] = value if old is None else combiner(old, value)


class Lights(object):
  def __init__(self, count):
    self._count = count

  def count(self):
    return self._count

  def output(self, index, color):
    pass


class Container(Lights):
  def __init__(self, lights):
    self.lights = lights

  def count(self):
    return self.lights.count()

  def output(self, index, color):
    return self.lights.output(index, color)


class Mapper(Container):
  def __init__(self, mapper, lights):
    super(Mapper, self).__init__(lights)
    self.mapper = mapper

  def output(self, index, color):
    return self.lights.output(self.mapper(index), color)


class Reverse(Container):
  def output(self, index, color):
    return self.lights.output(count - index - 1, color)




class Light(object):
  def __init__(self, index, update_table):
    self.index = index
    self.update_table = update_table

  def update(self, value):
    self.update_table.setdefault(self.index, []).append(value)


def light_strategy(light_count, cycle_index, total_cycle_count):
  # return an iteration of light/color pairs.
  pass



def time_insensitive_strategy(light_count):
  pass

def time_sensitive_strategy(light_count, time_length):
  def f(time):
    pass
  return f

def light_strategy(light_count, cycle_index, total_cycle_count):






def apply_lights()
