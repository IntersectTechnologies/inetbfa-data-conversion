"""
Contains backtesting logic and objects.
"""
from copy import deepcopy
import bt
import ffn
import pandas as pd
from matplotlib import pyplot as plt
from .performance import Result

def run(*backtests):
    """
    Runs a series of backtests and returns a Result
    object containing the results of the backtests.

    Args:
        * backtest (*list): List of backtests.

    Returns:
        Result

    """
    # run each backtest
    for bkt in backtests:
        bkt.run()

    return Result(*backtests)

class Backtest(object):

    """
    A Backtest combines a Strategy with data to
    produce a Result.

    A backtest is basically testing a strategy over a data set.

    Note:
        The Strategy will be deepcopied so it is re-usable in other
        backtests. To access the backtested strategy, simply access
        the strategy attribute.

    Args:
        * strategy (Strategy, Node, StrategyBase): The Strategy to be tested.
        * data (DataFrame or Panel): DataFrame or Panel containing data used in backtest. This
            will be the Strategy's "universe".  
            In case of a DataFrame the rows contains the dates 
            and the columns the tickers - the data is the price of each security
            In case of a Panel the major_axis contains the dates, the minor_axis the different
            metrics to be used in the back-test and the items are for each security
        * name (str): Backtest name - defaults to strategy name
        * initial_capital (float): Initial amount of capital passed to
            Strategy.
        * commission (fn(quantity)): The commission function to be used.

    Attributes:
        * strategy (Strategy): The Backtest's Strategy. This will be a deepcopy
            of the Strategy that was passed in.
        * data (DataFrame / Panel): Data passed in
        * dates (DateTimeIndex): Data's index
        * initial_capital (float): Initial capital
        * name (str): Backtest name
        * stats (ffn.PerformanceStats): Performance statistics
        * has_run (bool): Run flag
        * weights (DataFrame): Weights of each component over time
        * security_weights (DataFrame): Weights of each security as a
            percentage of the whole portfolio over time

    """

    def __init__(self, strategy, data,
                 name=None,
                 initial_capital=1000000.0,
                 commissions=None):

        # we want to reuse strategy logic - copy it!
        # basically strategy is a template
        self.strategy = deepcopy(strategy)
        
        assert type(data) == pd.DataFrame or type(data) == pd.Panel
        self.data = data
        self.dates = data.index
        
        
        self.initial_capital = initial_capital
        self.name = name if name is not None else strategy.name

        if commissions:
            self.strategy.set_commissions(commissions)

        self.stats = {}
        self._original_prices = None
        self._weights = None
        self._sweights = None
        self.has_run = False

    def run(self):
        """
        Runs the Backtest.
        """
        # set run flag
        self.has_run = True

        # setup strategy
        self.strategy.setup(self.data)

        # adjust strategy with initial capital
        self.strategy.adjust(self.initial_capital)

        # loop through dates
        for dt in self.dates:
            self.strategy.update(dt)
            self.strategy.run()
            # need update after to save weights, values and such
            self.strategy.update(dt)

        self.stats = self.strategy.prices.calc_perf_stats()
        self._original_prices = self.strategy.prices

    @property
    def weights(self):
        """
        DataFrame of  each component's weight over time
        """
        if self._weights is not None:
            return self._weights
        else:
            vals = pd.DataFrame({x.full_name: x.values for x in
                                 self.strategy.members})
            vals = vals.div(self.strategy.values, axis=0)
            self._weights = vals
            return vals

    @property
    def security_weights(self):
        """
        DataFrame containing weights of each security as a
        percentage of the whole portfolio over time
        """
        if self._sweights is not None:
            return self._sweights
        else:
            # get values for all securities in tree and divide by root values
            # for security weights
            vals = {}
            for m in self.strategy.members:
                if isinstance(m, bt.core.SecurityBase):
                    if m.name in vals:
                        vals[m.name] += m.values
                    else:
                        vals[m.name] = m.values
            vals = pd.DataFrame(vals)

            # divide by root strategy values
            vals = vals.div(self.strategy.values, axis=0)

            # save for future use
            self._sweights = vals

            return vals