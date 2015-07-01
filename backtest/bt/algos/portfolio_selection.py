# -*- coding: utf-8 -*-
#
# Copyright 2015 Intersect Technologies CC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Created on Tue Jan 20 09:24:27 2015

@author: Niel
"""

import bt
from bt.core import Algo, AlgoStack
import random
import numpy as np
import pandas as pd
import ffn

class WeighEqually(Algo):

    """
    Sets temp['weights'] by calculating equal weights for all items in
    selected.

    Equal weight Algo. Sets the 'weights' to 1/n for each item in 'selected'.

    Sets:
        * weights

    Requires:
        * selected

    """

    def __init__(self):
        super(WeighEqually, self).__init__()

    def __call__(self, target):
        selected = target.temp['selected']
        n = len(selected)

        if n == 0:
            target.temp['weights'] = {}
        else:
            w = 1.0 / n
            target.temp['weights'] = {x: w for x in selected}

        return True

class WeighSpecified(Algo):

    """
    Sets temp['weights'] based on a provided dict of ticker:weights.

    Sets the weights based on pre-specified targets.

    Args:
        * weights (dict): target weights -> ticker: weight

    Sets:
        * weights

    """

    def __init__(self, **weights):
        super(WeighSpecified, self).__init__()
        self.weights = weights

    def __call__(self, target):
        # added copy to make sure these are not overwritten
        target.temp['weights'] = self.weights.copy()
        return True


class WeighTarget(Algo):

    """
    Sets target weights based on a target weight DataFrame.

    If the target weight dataFrame is  of same dimension
    as the target.universe, the portfolio will effectively be rebalanced on each
    period. For example, if we have daily data and the target DataFrame is of
    the same shape, we will have daily rebalancing.

    However, if we provide a target weight dataframe that has only month end
    dates, then rebalancing only occurs monthly.

    Basically, if a weight is provided on a given date, the target weights are
    set and the algo moves on (presumably to a Rebalance algo). If not, not
    target weights are set.

    Args:
        * weights (DataFrame): DataFrame containing the target weights

    Sets:
        * weights

    """

    def __init__(self, weights):
        self.weights = weights

    def __call__(self, target):
        # get current target weights
        if target.now in self.weights.index:
            w = self.weights.ix[target.now]

            # dropna and save
            target.temp['weights'] = w.dropna()

        return True


class WeighInvVol(Algo):

    """
    Sets temp['weights'] based on the inverse volatility Algo.

    Sets the target weights based on ffn's calc_inv_vol_weights. This
    is a commonly used technique for risk parity portfolios. The least
    volatile elements receive the highest weight under this scheme. Weights
    are proportional to the inverse of their volatility.

    Args:
        * lookback (DateOffset): lookback period for estimating volatility

    Sets:
        * weights

    Requires:
        * selected

    """

    def __init__(self, lookback=pd.DateOffset(months=3)):
        super(WeighInvVol, self).__init__()
        self.lookback = lookback

    def __call__(self, target):
        selected = target.temp['selected']

        if len(selected) == 0:
            target.temp['weights'] = {}
            return True

        if len(selected) == 1:
            target.temp['weights'] = {selected[0]: 1.}
            return True

        prc = target.universe[selected].ix[target.now - self.lookback:]
        tw = bt.ffn.calc_inv_vol_weights(
            prc.to_returns().dropna())
        target.temp['weights'] = tw.dropna()
        return True


class WeighMeanVar(Algo):

    """
    Sets temp['weights'] based on mean-variance optimization.

    Sets the target weights based on ffn's calc_mean_var_weights. This is a
    Python implementation of Markowitz's mean-variance optimization.

    See:
        http://en.wikipedia.org/wiki/Modern_portfolio_theory#The_efficient_frontier_with_no_risk-free_asset

    Args:
        * lookback (DateOffset): lookback period for estimating volatility
        * bounds ((min, max)): tuple specifying the min and max weights for
            each asset in the optimization.
        * covar_method (str): method used to estimate the covariance. See ffn's
            calc_mean_var_weights for more details.
        * rf (float): risk-free rate used in optimization.

    Sets:
        * weights

    Requires:
        * selected

    """

    def __init__(self, lookback=pd.DateOffset(months=3),
                 bounds=(0., 1.), covar_method='ledoit-wolf',
                 rf=0.):
        super(WeighMeanVar, self).__init__()
        self.lookback = lookback
        self.bounds = bounds
        self.covar_method = covar_method
        self.rf = rf

    def __call__(self, target):
        selected = target.temp['selected']

        if len(selected) == 0:
            target.temp['weights'] = {}
            return True

        if len(selected) == 1:
            target.temp['weights'] = {selected[0]: 1.}
            return True

        prc = target.universe[selected].ix[target.now - self.lookback:]
        tw = bt.ffn.calc_mean_var_weights(
            prc.to_returns().dropna(), weight_bounds=self.bounds,
            covar_method=self.covar_method, rf=self.rf)

        target.temp['weights'] = tw.dropna()
        return True


class WeighRandomly(Algo):

    """
    Sets temp['weights'] based on a random weight vector.

    Sets random target weights for each security in 'selected'.
    This is useful for benchmarking against a strategy where we believe
    the weighing algorithm is adding value.

    For example, if we are testing a low-vol strategy and we want to see if
    our weighing strategy is better than just weighing
    securities randomly, we could use this Algo to create a random Strategy
    used for random benchmarking.

    This is an Algo wrapper around ffn's random_weights function.

    Args:
        * bounds ((low, high)): Tuple including low and high bounds for each
            security
        * weight_sum (float): What should the weights sum up to?

    Sets:
        * weights

    Requires:
        * selected

    """

    def __init__(self, bounds=(0., 1.), weight_sum=1):
        super(WeighRandomly, self).__init__()
        self.bounds = bounds
        self.weight_sum = weight_sum

    def __call__(self, target):
        sel = target.temp['selected']
        n = len(sel)

        w = {}
        try:
            rw = bt.ffn.random_weights(
                n, self.bounds, self.weight_sum)
            w = dict(zip(sel, rw))
        except ValueError:
            pass

        target.temp['weights'] = w
        return True
        
def equal_weighted(portfolio):
    '''
    Calculate the weights for an equally weighted portfolio
    100 / n - where n is the number of instruments in the portfolio
    
    Parameters
    ----------
    portfolio : pandas.core.index.Index
    
    Returns
    -------
    weights : pandas.core.series.Series
    '''
	
def value_weighted(portfolio, marketcap):
    '''
    Calculate the weights for a value (Market Cap) weighted portfolio
    
    Parameters
    ---------
    portfolio : pandas.core.index.Index
    
    marketcap : pandas.core.series.Series
    
    Returns
    -------
    weights : pandas.core.series.Series

    '''
    
    assert type(portfolio) == pd.core.index.Index
    
    tot_mc = marketcap[portfolio.index].sum()
    weights = marketcap[portfolio.index]/tot_mc
    return weights

def minimum_variance(security_returns, weight_bounds):
    '''
    
    Parameters
    ----------
    
    Returns
    -------
    
    
    '''

def mean_variance_optimal(security_returns, riskfree_rate, weight_bounds):
    '''
    Calculates the optimal mean-variance weights for a portfolio given a DataFrame of security returns.
    The lower and upper bound of weights can be specified as well as the risk-free rate to calculate 
    the point on the efficient frontier that maiximizes the Sharpe Ratio.
    
    The expected returns of each security is calculated as the mean historical
    
    Parameters
    ----------
    portf_returns : pandas.core.frame.DataFrame
        Returns for multiple securities
    
    riskfree_rate : float
        Risk-free rate used in utility calculation
    
    weight_bounds : array or list of tuple s
        (lower_bound, upper_bound)
    
    Returns
    -------
    weights : pandas.core.series.Series
    '''
    
    ffn.calc_mean_var_weights(returns, weight_bounds, riskfree_rate, covar_method = 'ledoit_wolf')
    
def inverse_volatility_weighted(portfolio):
    '''
    '''
    
def random_weights(portfolio):
    '''
    '''
    
	
def liquidity_weighted():
    	'''
    	Calculate the weights for a liquidity weighted portfolio.
    	
    	
    	'''