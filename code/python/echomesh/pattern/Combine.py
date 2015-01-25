from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.pattern.Pattern import Pattern

class Combine(Pattern):
    HELP = 'Combine patterns.'

    SETTINGS = {
        'combine': {
            'default': 'add',
            'literal': True,
            'help': 'Name of a function to apply to each pixel',
            'constant': True,
            },
        'keywords': {
            'default': {},
            'literal': True,
            'constant': True,
            'help': 'Keyword arguments to the combiner',
            }
        }

    COMBINERS = {
        'add' : cechomesh.combine_color_lists
        }

    def _precompute(self):
        combine = self.get('combine')
        try:
            self.combine = COMBINERS[combine]
        except:
            raise Exception('Didn\'t understand combiner "%s".' % combine)
        self.keywords = self.get('keywords')

    def _evaluate(self):
        return self.combine(self._patterns, **self.keywords)
