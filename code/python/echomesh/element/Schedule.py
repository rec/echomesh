from __future__ import absolute_import, division, print_function, unicode_literals

# TODO: needs to be finished and integrated into the code.

import parsedatetime

from echomesh.element import Element
from echomesh.element import Load

CALENDAR = parsedatetime.Calendar()

BAD_DOCUMENTATION = """
type: schedule

entry:
  -
    begin: 10:14
    end: 10:55
    length: 0:23
    repeat: daily, none, weekly, absolute
    priority: 5
    elements: something
"""

class Entry(object):
  def __init__(self, schedule, begin=None, end=None, length=None, repeat=None,
               priority=None, element=None):

    self.begin = begin and CALENDAR.parse(begin)
    self.end = end and CALENDAR.parse(end)
    self.length = length
    self.repeat = repeat
    self.priority = priority


class Schedule(Element.Element):
  def __init__(self, parent, description):
    super(Schedule, self).__init__(parent, description)
    entries = description.get('entries', [])
    self.entries = [Entry(self, *e) for e in entries]
    self.current_priority = 0
