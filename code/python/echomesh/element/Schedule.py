from __future__ import absolute_import, division, print_function, unicode_literals

# TODO: needs to be finished and integrated into the code.

import parsedatetime

from echomesh.base import Config
from echomesh.element import Element
from echomesh.element import Load
from echomesh.util import Log

LOGGER = Log.logger(__name__)

CALENDAR = parsedatetime.Calendar()

"""
type: schedule

entry:
  -
    begin: 10:14
    end: 10:55
    length: 0:23
    repeat: daily, none, weekly, absolute
    priority: 5
    element: something
"""

class Entry(object):
  def __init__(self, schedule, begin=None, end=None, length=None, repeat=None,
               priority=None, element=None):

    self.begin = begin and CALENDAR.parse(begin)
    self.end = end and CALENDAR.parse(end)
    self.length = length
    self.repeat = repeat
    self.priority = priority
    self.element = Load.make_one(schedule, element)


class Schedule(Element.Element):
  def __init__(self, parent, description):
    super(Schedule, self).__init__(parent, description)
    entries = description.get('entries', [])
    self.entries = [Entry(self, *e) for e in entries]
    self.current_priority = 0

Element.register(Schedule)
