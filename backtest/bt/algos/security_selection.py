# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 17:28:35 2015

@author: Niel
"""

import pandas as pd
import bt
from bt.core import Algo, AlgoStack
import random


class SelectAll(Algo):

    """
    Sets temp['selected'] with all securities (based on universe).

    Selects all the securities and saves them in temp['selected'].
    By default, SelectAll does not include securities that have no
    data (nan) on current date.

    Args:
        * include_no_data (bool): Include securities that do not have data?

    Sets:
        * selected

    """

    def __init__(self, include_no_data=False):
        super(SelectAll, self).__init__()
        self.include_no_data = include_no_data

    def __call__(self, target):
        if self.include_no_data:
            target.temp['selected'] = target.universe.columns
        else:
            target.temp['selected'] = list(
                target.universe.ix[target.now].dropna().index)
        return True

class SelectThese(Algo):

    """
    Sets temp['selected'] with a set list of tickers.

    Sets the temp['selected'] to a set list of tickers.

    Args:
        * ticker (list): List of tickers to select.

    Sets:
        * selected

    """

    def __init__(self, tickers):
        super(SelectThese, self).__init__()
        self.tickers = tickers

    def __call__(self, target):
        target.temp['selected'] = self.tickers
        return True

class SelectHasData(Algo):

    """
    Sets temp['selected'] based on all items in universe that meet
    data requirements.

    This is a more advanced version of SelectAll. Useful for selecting
    tickers that need a certain amount of data for future algos to run
    properly.

    For example, if we need the items with 3 months of data or more,
    we could use this Algo with a lookback period of 3 months.

    When providing a lookback period, it is also wise to provide a min_count.
    This is basically the number of data points needed within the lookback
    period for a series to be considered valid. For example, in our 3 month
    lookback above, we might want to specify the min_count as being
    57 -> a typical trading month has give or take 20 trading days. If we
    factor in some holidays, we can use 57 or 58. It's really up to you.

    If you don't specify min_count, min_count will default to ffn's
    get_num_days_required.

    Args:
        * lookback (DateOffset): A DateOffset that determines the lookback
            period.
        * min_count (int): Minimum number of days required for a series to be
            considered valid. If not provided, ffn's get_num_days_required is
            used to estimate the number of points required.

    Sets:
        * selected

    """

    def __init__(self, lookback=pd.DateOffset(months=3),
                 min_count=None):
        super(SelectHasData, self).__init__()
        self.lookback = lookback
        if min_count is None:
            min_count = bt.ffn.get_num_days_required(lookback)
        self.min_count = min_count

    def __call__(self, target):
        if 'selected' in target.temp:
            selected = target.temp['selected']
        else:
            selected = target.universe.columns

        filt = target.universe[selected].ix[target.now - self.lookback:]
        cnt = filt.count()
        cnt = cnt[cnt >= self.min_count]
        target.temp['selected'] = list(cnt.index)
        return True

class SelectN(Algo):

    """
    Sets temp['selected'] based on ranking temp['stat'].

    Selects the top or botton N items based on temp['stat'].
    This is usually some kind of metric that will be computed in a
    previous Algo and will be used for ranking purposes. Can select
    top or bottom N based on sort_descending parameter.

    Args:
        * n (int): select top n items.
        * sort_descending (bool): Should the stat be sorted in descending order
            before selecting the first n items?
        * all_or_none (bool): If true, only populates temp['selected'] if we
            have n items. If we have less than n, then temp['selected'] = [].

    Sets:
        * selected

    Requires:
        * stat

    """

    def __init__(self, n, sort_descending=True,
                 all_or_none=False):
        super(SelectN, self).__init__()
        if n < 0:
            raise ValueError('n cannot be negative')
        self.n = n
        self.ascending = not sort_descending
        self.all_or_none = all_or_none

    def __call__(self, target):
        stat = target.temp['stat']
        stat.sort(ascending=self.ascending)

        # handle percent n
        keep_n = self.n
        if self.n < 1:
            keep_n = int(self.n * len(stat))

        sel = list(stat[:keep_n].index)

        if self.all_or_none and len(sel) < keep_n:
            sel = []

        target.temp['selected'] = sel

        return True
   
class SelectMomentum(AlgoStack):

    """
    Sets temp['selected'] based on a simple momentum filter.

    Selects the top n securities based on the total return over
    a given lookback period. This is just a wrapper around an
    AlgoStack with two algos: StatTotalReturn and SelectN.

    Args:
        * n (int): select first N elements
        * lookback (DateOffset): lookback period for total return
            calculation
        * sort_descending (bool): Sort descending (highest return is best)

    Sets:
        * selected

    Requires:
        * selected

    """

    def __init__(self, n, lookback=pd.DateOffset(months=3),
                 sort_descending=True):
        super(SelectMomentum, self).__init__(
            StatTotalReturn(lookback=lookback),
            SelectN(n=n, sort_descending=sort_descending))

class SelectWhere(Algo):

    """
    Selects securities based on an indicator DataFrame.

    Selects securities where the value is True on the current date
    (target.now) only if current date is present in signal DataFrame.

    For example, this could be the result of a pandas boolean comparison such
    as data > 100.

    Args:
        * signal (DataFrame): Boolean DataFrame containing selection logic.

    Sets:
        * selected

    """

    def __init__(self, signal):
        self.signal = signal

    def __call__(self, target):
        # get signal Series at target.now
        if target.now in self.signal.index:
            sig = self.signal.ix[target.now]
            # get tickers where True
            selected = sig.index[sig]
            # save as list
            target.temp['selected'] = list(selected)

        return True

class SelectRandomly(AlgoStack):

    """
    Sets temp['selected'] based on a random subset of
    the items currently in temp['selected'].

    Selects n random elements from the list stored in temp['selected'].
    This is useful for benchmarking against a strategy where we believe
    the selection algorithm is adding value.

    For example, if we are testing a momentum strategy and we want to see if
    selecting securities based on momentum is better than just selecting
    securities randomly, we could use this Algo to create a random Strategy
    used for random benchmarking.

    Note:
        Another selection algorithm should be use prior to this Algo to
        populate temp['selected']. This will typically be SelectAll.

    Args:
        * n (int): Select N elements randomly.

    Sets:
        * selected

    Requires:
        * selected

    """

    def __init__(self, n=None):
        super(SelectRandomly, self).__init__()
        self.n = n

    def __call__(self, target):
        sel = target.temp['selected']

        if self.n is not None:
            sel = random.sample(sel, self.n)

        target.temp['selected'] = sel
        return True
