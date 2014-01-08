import re

LINE_RE = re.compile(r'\s*namer.add\("(.*)", 0x(.*)\);.*')

with open('/tmp/colors.txt') as f:
  data = {}
  for line in f:
    matches = LINE_RE.match(line)
    if matches:
      color, number = matches.groups()
      if len(number) < 8:
        number = 'ff%s' % number
      data[color] = number
    else:
      print 'ERROR: don\'t understand:', line
  inverse = {}
  dupes = {}
  for color, number in sorted(data.iteritems()):
    if number in inverse:
      dupes.setdefault(number, []).append(color)
    else:
      inverse[number] = color
    print '  namer.add("%s", 0x%s);' % (color, number)

  if dupes:
    print dupes
    for number, colors in dupes.iteritems():
      print '%s -> %s (originally %s)' % (number, colors, inverse[number])
