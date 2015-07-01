# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 17:51:29 2015

@author: Niel
"""
import bt
from bt.core import Algo, AlgoStack
import pandas as pd

class StatTotalReturn(Algo):

    """
    Sets temp['stat'] with total returns over a given period.

    Sets the 'stat' based on the total return of each element in
    temp['selected'] over a given lookback period. The total return
    is determined by ffn's calc_total_return.

    Args:
        * lookback (DateOffset): lookback period.

    Sets:
        * stat

    Requires:
        * selected

    """

    def __init__(self, lookback=pd.DateOffset(months=3)):
        super(StatTotalReturn, self).__init__()
        self.lookback = lookback

    def __call__(self, target):
        selected = target.temp['selected']
        prc = target.universe[selected].ix[target.now - self.lookback:]
        target.temp['stat'] = prc.calc_total_return()
        return True