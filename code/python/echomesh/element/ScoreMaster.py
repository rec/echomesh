class Scores(MasterRunnable.MasterRunnable):
  def __init__(self):
    super(Scores, self).__init__()
    self.scores = {}

  def start(self):
    self.is_running = True

  def make_score(self, scorefile):
    elements = Load.load(scorefile)
    if not elements:
      raise Exception('Unable to open score file %s' % scorefile)
    description = {'elements': elements, 'type': 'score'}
    score = Score(None, description)
    name = self._make_name(scorefile)
    self.scores[name] = score
    score.name = name
    return score

  def _make_name(self, scorefile):
    while scorefile in self.elements:
      match = MATCH_NAME.match(scorefile)
      if match:
        base, suffix = match.groups()
        suffix = str(1 + int(suffix))
      else:
        base, suffix = score_file, '0'
      scorefile = '%s.%d' % (base, suffix)

    return scorefile

