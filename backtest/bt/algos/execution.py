# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 17:29:22 2015

@author: Niel
"""

import bt
from bt.core import Algo, AlgoStack
import pandas as pd
import numpy as np
import random

class Rebalance(Algo):

    """
    Rebalances capital based on temp['weights']

    Rebalances capital based on temp['weights']. Also closes
    positions if open but not in target_weights. This is typically
    the last Algo called once the target weights have been set.

    Requires:
        * weights

    """

    def __init__(self):
        super(Rebalance, self).__init__()

    def __call__(self, target):
        if 'weights' not in target.temp:
            return True

        targets = target.temp['weights']

        # de-allocate children that are not in targets
        not_in = [x for x in target.children if x not in targets]
        for c in not_in:
            target.close(c)

        # save value because it will change after each call to allocate
        # use it as base in rebalance calls
        base = target.value
        for item in targets.iteritems():
            target.rebalance(item[1], child=item[0], base=base)

        return True


class RebalanceOverTime(Algo):

    """
    Similar to Rebalance but rebalances to target
    weight over n periods.

    Rebalances towards a target weight over a n periods. Splits up the weight
    delta over n periods.

    This can be useful if we want to make more conservative rebalacing
    assumptions. Some strategies can produce large swings in allocations. It
    might not be reasonable to assume that this rebalancing can occur at the
    end of one specific period. Therefore, this algo can be used to simulate
    rebalancing over n periods.

    This has typically been used in monthly strategies where we want to spread
    out the rebalancing over 5 or 10 days.

    Note:
        This Algo will require the run_always wrapper in the above case. For
        example, the RunMonthly will return True on the first day, and
        RebalanceOverTime will be 'armed'. However, RunMonthly will return
        False the rest days of the month. Therefore, we must specify that we
        want to always run this algo.

    Args:
        * n (int): number of periods over which rebalancing takes place.

    Requires:
        * weights

    """

    def __init__(self, n=10):
        super(RebalanceOverTime, self).__init__()
        self.n = float(n)
        self._rb = Rebalance()
        self._weights = None
        self._days_left = None

    def __call__(self, target):
        # new weights specified - update rebalance data
        if 'weights' in target.temp:
            self._weights = target.temp['weights']
            self._days_left = self.n

        # if _weights are not None, we have some work to do
        if self._weights is not None:
            tgt = {}
            # scale delta relative to # of periods left and set that as the new
            # target
            for t in self._weights:
                curr = target.children[t].weight if t in \
                    target.children else 0.
                dlt = (self._weights[t] - curr) / self._days_left
                tgt[t] = curr + dlt

            # mock weights and call real Rebalance
            target.temp['weights'] = tgt
            self._rb(target)

            # dec _days_left. If 0, set to None & set _weights to None
            self._days_left -= 1

            if self._days_left == 0:
                self._days_left = None
                self._weights = None

        return True
