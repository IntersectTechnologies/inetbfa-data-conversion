"""
A collection of Algos used to create Strategy logic.
"""
import bt
from bt.core import Algo, AlgoStack
import pandas as pd
import numpy as np
import random

def run_always(f):
    """
    Run always decorator to be used with Algo
    to ensure stack runs the decorated Algo
    on each pass, regardless of failures in the stack.
    """
    f.run_always = True
    return f


class PrintDate(Algo):

    """
    This Algo simply print's the current date.

    Can be useful for debugging purposes.
    """

    def __call__(self, target):
        print target.now
        return True


class PrintTempData(Algo):

    """
    This Algo prints the temp data.

    Useful for debugging.
    """

    def __call__(self, target):
        print target.temp
        return True


class RunOnce(Algo):

    """
    Returns True on first run then returns False.

    As the name says, the algo only runs once. Useful in situations
    where we want to run the logic once (buy and hold for example).
    """

    def __init__(self):
        super(RunOnce, self).__init__()
        self.has_run = False

    def __call__(self, target):
        # if it hasn't run then we will
        # run it and set flag
        if not self.has_run:
            self.has_run = True
            return True

        # return false to stop future execution
        return False


class RunWeekly(Algo):

    """
    Returns True on week change.

    Returns True if the target.now's week has changed
    since the last run, if not returns False. Useful for
    weekly rebalancing strategies.

    Note:
        This algo will typically run on the first day of the
        week (assuming we have daily data)

    """

    def __init__(self):
        super(RunWeekly, self).__init__()
        self.last_date = None

    def __call__(self, target):
        # get last date
        now = target.now

        # if none nothing to do - return false
        if now is None:
            return False

        # create pandas.Timestamp for useful .week property
        now = pd.Timestamp(now)

        if self.last_date is None:
            self.last_date = now
            return False

        result = False
        if now.week != self.last_date.week:
            result = True

        self.last_date = now
        return result


class RunMonthly(Algo):

    """
    Returns True on month change.

    Returns True if the target.now's month has changed
    since the last run, if not returns False. Useful for
    monthly rebalancing strategies.

    Note:
        This algo will typically run on the first day of the
        month (assuming we have daily data)

    """

    def __init__(self):
        super(RunMonthly, self).__init__()
        self.last_date = None

    def __call__(self, target):
        # get last date
        now = target.now

        # if none nothing to do - return false
        if now is None:
            return False

        if self.last_date is None:
            self.last_date = now
            return False

        result = False
        if now.month != self.last_date.month:
            result = True

        self.last_date = now
        return result


class RunQuarterly(Algo):

    """
    Returns True on quarter change.

    Returns True if the target.now's month has changed
    since the last run and the month is the first month
    of the quarter, if not returns False. Useful for
    quarterly rebalancing strategies.

    Note:
        This algo will typically run on the first day of the
        quarter (assuming we have daily data)

    """

    def __init__(self):
        super(RunQuarterly, self).__init__()
        self.last_date = None

    def __call__(self, target):
        # get last date
        now = target.now

        # if none nothing to do - return false
        if now is None:
            return False

        if self.last_date is None:
            self.last_date = now
            return False

        result = False
        if now.month != self.last_date.month and now.month % 3 == 1:
            result = True

        self.last_date = now
        return result


class RunYearly(Algo):

    """
    Returns True on year change.

    Returns True if the target.now's year has changed
    since the last run, if not returns False. Useful for
    yearly rebalancing strategies.

    Note:
        This algo will typically run on the first day of the
        year (assuming we have daily data)

    """

    def __init__(self):
        super(RunYearly, self).__init__()
        self.last_date = None

    def __call__(self, target):
        # get last date
        now = target.now

        # if none nothing to do - return false
        if now is None:
            return False

        if self.last_date is None:
            self.last_date = now
            return False

        result = False
        if now.year != self.last_date.year:
            result = True

        self.last_date = now
        return result


class RunOnDate(Algo):

    """
    Returns True on a specific set of dates.

    Args:
        * dates (list): List of dates to run Algo on.

    """

    def __init__(self, *dates):
        """
        Args:
            * dates (*args): A list of dates. Dates will be parsed
                by pandas.to_datetime so pass anything that it can
                parse. Typically, you will pass a string 'yyyy-mm-dd'.
        """
        super(RunOnDate, self).__init__()
        # parse dates and save
        self.dates = [pd.to_datetime(d) for d in dates]

    def __call__(self, target):
        return target.now in self.dates

class RunAfterDate(Algo):

    """
    Returns True after a date has passed

    Args:
        * date: Date after which to start trading

    Note:
        This is useful for algos that rely on trailing averages where you
        don't want to start trading until some amount of data has been built up

    """

    def __init__(self, date):
        """
        Args:
            * date: Date after which to start trading
        """
        super(RunAfterDate, self).__init__()
        # parse dates and save
        self.date = pd.to_datetime(date)

    def __call__(self, target):
        return target.now > self.date

class RunAfterDays(Algo):

    """
    Returns True after a specific number of 'warmup' trading days have passed

    Args:
        * days (int): Number of trading days to wait before starting

    Note:
        This is useful for algos that rely on trailing averages where you
        don't want to start trading until some amount of data has been built up

    """

    def __init__(self, days):
        """
        Args:
            * days (int): Number of trading days to wait before starting
        """
        super(RunAfterDays, self).__init__()
        self.days = days

    def __call__(self, target):
        if self.days > 0:
            self.days -= 1
            return False
        return True


class CapitalFlow(Algo):

    """
    Used to model capital flows. Flows can either be inflows or outflows.

    This Algo can be used to model capital flows. For example, a pension
    fund might have inflows every month or year due to contributions. This
    Algo will affect the capital of the target node without affecting returns
    for the node.

    Since this is modeled as an adjustment, the capital will remain in the
    strategy until a re-allocation/rebalancement is made.

    Args:
        * amount (float): Amount of adjustment

    """

    def __init__(self, amount):
        """
        CapitalFlow constructor.

        Args:
            * amount (float): Amount to adjust by
        """
        super(CapitalFlow, self).__init__()
        self.amount = float(amount)

    def __call__(self, target):
        target.adjust(self.amount)
        return True

class Require(Algo):

    """
    Flow control Algo.

    This algo returns the value of a predicate
    on an temp entry. Useful for controlling
    flow.

    For example, we might want to make sure we have some items selected.
    We could pass a lambda function that checks the len of 'selected':

        pred=lambda x: len(x) == 0
        item='selected'

    Args:
        * pred (Algo): Function that returns a Bool given the strategy. This
            is the definition of an Algo. However, this is typically used
            with a simple lambda function.
        * item (str): An item within temp.
        * if_none (bool): Result if the item required is not in temp or if it's
            value if None

    """

    def __init__(self, pred, item, if_none=False):
        super(Require, self).__init__()
        self.item = item
        self.pred = pred
        self.if_none = if_none

    def __call__(self, target):
        if self.item not in target.temp:
            return self.if_none

        item = target.temp[self.item]

        if item is None:
            return self.if_none

        return self.pred(item)
