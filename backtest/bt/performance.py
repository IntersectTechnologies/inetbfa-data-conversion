# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 19:42:39 2015

@author: Niel
"""

import ffn
import pandas as pd
from matplotlib import pyplot as plt

def benchmark_random(backtest, random_strategy, nsim=100):
    """
    Given a backtest and a random strategy, compare backtest to
    a number of random portfolios.

    The idea here is to benchmark your strategy vs a bunch of
    random strategies that have a similar structure but execute
    some part of the logic randomly - basically you are trying to
    determine if your strategy has any merit - does it beat
    randomly picking weight? Or randomly picking the selected
    securities?

    Args:
        * backtest (Backtest): A backtest you want to benchmark
        * random_strategy (Strategy): A strategy you want to benchmark
            against. The strategy should have a random component to
            emulate skilless behavior.
        * nsim (int): number of random strategies to create.

    Returns:
        RandomBenchmarkResult

    """
    # save name for future use
    if backtest.name is None:
        backtest.name = 'original'

    # run if necessary
    if not backtest.has_run:
        backtest.run()

    bts = []
    bts.append(backtest)
    data = backtest.data

    # create and run random backtests
    for i in range(nsim):
        random_strategy.name = 'random_%s' % i
        rbt = bt.Backtest(random_strategy, data)
        rbt.run()

        bts.append(rbt)

    # now create new RandomBenchmarkResult
    res = RandomBenchmarkResult(*bts)

    return res
    
class Result(ffn.GroupStats):

    """
    Based on ffn's GroupStats with a few extra helper methods.

    Args:
        * backtests (list): List of backtests

    Attributes:
        * backtest_list (list): List of bactests in the same order as provided
        * backtests (dict): Dict of backtests by name

    """

    def __init__(self, *backtests):
        tmp = [pd.DataFrame({x.name: x.strategy.prices}) for x in backtests]
        super(Result, self).__init__(*tmp)
        self.backtest_list = backtests
        self.backtests = {x.name: x for x in backtests}

    def display_monthly_returns(self, backtest=0):
        """
        Display monthly returns for a specific backtest.

        Args:
            * backtest (str, int): Backtest. Can be either a index (int) or the
                name (str)

        """
        key = self._get_backtest(backtest)
        self[key].display_monthly_returns()

    def plot_weights(self, backtest=0, filter=None,
                     figsize=(15, 5), **kwds):
        """
        Plots the weights of a given backtest over time.

        Args:
            * backtest (str, int): Backtest. Can be either a index (int) or the
                name (str)
            * filter (list, str): filter columns for specific columns. Filter
                is simply passed as is to DataFrame[filter], so use something
                that makes sense with a DataFrame.
            * figsize ((width, height)): figure size
            * kwds (dict): Keywords passed to plot

        """
        key = self._get_backtest(backtest)

        if filter is not None:
            data = self.backtests[key].weights[filter]
        else:
            data = self.backtests[key].weights

        data.plot(figsize=figsize, **kwds)

    def plot_security_weights(self, backtest=0, filter=None,
                              figsize=(15, 5), **kwds):
        """
        Plots the security weights of a given backtest over time.

        Args:
            * backtest (str, int): Backtest. Can be either a index (int) or the
                name (str)
            * filter (list, str): filter columns for specific columns. Filter
                is simply passed as is to DataFrame[filter], so use something
                that makes sense with a DataFrame.
            * figsize ((width, height)): figure size
            * kwds (dict): Keywords passed to plot

        """
        key = self._get_backtest(backtest)

        if filter is not None:
            data = self.backtests[key].security_weights[filter]
        else:
            data = self.backtests[key].security_weights

        data.plot(figsize=figsize, **kwds)

    def plot_histogram(self, backtest=0, **kwds):
        """
        Plots the return histogram of a given backtest over time.

        Args:
            * backtest (str, int): Backtest. Can be either a index (int) or the
                name (str)
            * kwds (dict): Keywords passed to plot_histogram

        """
        key = self._get_backtest(backtest)
        self[key].plot_histogram(**kwds)

    def _get_backtest(self, backtest):
        # based on input order
        if type(backtest) == int:
            return self.backtest_list[backtest].name

        # default case assume ok
        return backtest


class RandomBenchmarkResult(Result):

    """
    RandomBenchmarkResult expands on Result to add methods specific
    to random strategy benchmarking.

    Args:
        * backtests (list): List of backtests

    Attributes:
        * base_name (str): Name of backtest being benchmarked
        * r_stats (Result): Stats for random strategies
        * b_stats (Result): Stats for benchmarked strategy

    """

    def __init__(self, *backtests):
        super(RandomBenchmarkResult, self).__init__(*backtests)
        self.base_name = backtests[0].name
        # seperate stats to make
        self.r_stats = self.stats.drop(self.base_name, axis=1)
        self.b_stats = self.stats[self.base_name]

    def plot_histogram(self, statistic='monthly_sharpe',
                       figsize=(15, 5), title=None,
                       bins=20, **kwargs):
        """
        Plots the distribution of a given statistic. The histogram
        represents the distribution of the random strategies' statistic
        and the vertical line is the value of the benchmarked strategy's
        statistic.

        This helps you determine if your strategy is statistically 'better'
        than the random versions.

        Args:
            * statistic (str): Statistic - any numeric statistic in
                Result is valid.
            * figsize ((x, y)): Figure size
            * title (str): Chart title
            * bins (int): Number of bins
            * kwargs (dict): Passed to pandas hist function.

        """
        if not statistic in self.r_stats.index:
            raise ValueError("Invalid statistic. Valid statistics"
                             "are the statistics in self.stats")

        if title is None:
            title = '%s histogram' % statistic

        plt.figure(figsize=figsize)

        ser = self.r_stats.ix[statistic]

        ax = ser.hist(bins=bins, figsize=figsize, normed=True, **kwargs)
        ax.set_title(title)
        plt.axvline(self.b_stats[statistic], linewidth=4)
        ser.plot(kind='kde')
