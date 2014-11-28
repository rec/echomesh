from __future__ import absolute_import, division, print_function, unicode_literals

import bisect
import random

class WeightedRandom(object):
    def __init__(self, weights):
        assert weights
        total_weight, weights_counted = 0, 0
        self.totals = []
        for weight in weights:
            if weight is not None:
                assert weight >= 0, "Select weights can't be negative"
                weights_counted += 1
                total_weight += weight
            self.totals.append(weight)

        if not weights_counted:
            total_weight, weights_counted = 1, 1
        mean_weight = total_weight / weights_counted
        total_weight = 0
        for i, w in enumerate(self.totals):
            total_weight += (mean_weight if w is None else w)
            self.totals[i] = total_weight

    def select(self, random_value=None):
        if random_value is None:
            random_value = random.random()
        rnd = random_value * self.totals[-1]
        return bisect.bisect_right(self.totals, rnd)
