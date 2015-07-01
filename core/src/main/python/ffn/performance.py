"""
Created on Tue Feb 17 11:57:01 2015

@author: Niel
"""

import numpy as np
import pandas as pd
import random
import ffn.utils as utils
from ffn.utils import fmtp, fmtn, fmtpn, get_period_name
from pandas.core.base import PandasObject
from tabulate import tabulate
from matplotlib import pyplot as plt
import sklearn.manifold
import sklearn.cluster
import sklearn.covariance
from scipy.optimize import minimize
from scipy.stats import t
from ffn.utils import tolerant_equals

# Utils
def year_frac(start, end):
    """
    Similar to excel's yearfrac function. Returns
    a year fraction between two dates (i.e. 1.53 years).

    Approximation using the average number of seconds
    in a year.

    Args:
        * start (datetime): start date
        * end (datetime): end date

    """
    if start > end:
        raise ValueError('start cannot be larger than end')

    # obviously not perfect but good enough
    return (end - start).total_seconds() / (31557600)

# Performance
def calc_prob_mom(returns, other_returns):
    """
    Probabilistic momentum

    Basically the "probability or confidence that one asset
    is going to outperform the other".

    Source:
        http://cssanalytics.wordpress.com/2014/01/28/are-simple-momentum-strategies-too-dumb-introducing-probabilistic-momentum/ # NOQA
    """
    return t.cdf(returns.calc_information_ratio(other_returns),
                 len(returns) - 1)

def calc_total_return(prices):
    """
    Calculates the total return of a series.

    last / first - 1
    """
    return (prices.ix[-1] / prices.ix[0]) - 1

def calc_active_premium(portf_returns, benchmark_returns):
    '''
    
    Parameters
    ----------
    
    Returns
    -------
    
    
    '''
    relative_returns = portf_returns - benchmark_returns
    return np.mean(relative_returns)

def calc_cagr(prices):
    """
    Calculates the CAGR (compound annual growth rate) for a given price series.

    Args:
        * prices (pandas.TimeSeries): A TimeSeries of prices.
    Returns:
        * float -- cagr.

    """
    start = prices.index[0]
    end = prices.index[-1]
    return (prices.ix[-1] / prices.ix[0]) ** (1 / year_frac(start, end)) - 1
                 
# Risk/Return Ratios
def calc_sharpe_ratio(portf_return, riskfree_return, portf_volatility):
    """
    http://en.wikipedia.org/wiki/Sharpe_ratio
    
    Parameters
    ----------
        portf_return (float): Algorithm return percentage.
        riskfree_return (float): Treasury return percentage.
        portf_volatility (float): Algorithm volatility.

    Returns
    -------
        The Sharpe ratio (float) : 
    """
    if tolerant_equals(portf_volatility, 0):
        return np.nan

    return (portf_return - riskfree_return) / portf_volatility

def calc_sortino_ratio(portf_returns, riskfree_returns, mar):
    """
    http://en.wikipedia.org/wiki/Sortino_ratio

    Parameters
    ----------
        algorithm_returns (np.array-like):
            Returns from algorithm lifetime.
        algorithm_period_return (float):
            Algorithm return percentage from latest period.
        mar (float): Minimum acceptable return.

    Returns
    -------
        float. The Sortino ratio.
    """
    if tolerant_equals(mar, 0):
        return 0.0
    
    return (portf_returns - riskfree_returns) / mar

def calc_risk_return_ratio(self):
    """
    Calculates the return / risk ratio. Basically the
    Sharpe ratio without factoring in the risk-free rate.
    """
    return self.mean() / self.std()
    
def calc_information_ratio(returns, benchmark_returns):
    """
    http://en.wikipedia.org/wiki/Information_ratio
    
    Parameters
    ----------
    portf_returns (np.array-like):
        All returns during algorithm lifetime.
    benchmark_returns (np.array-like):
        All benchmark returns during algo lifetime.

    Returns
    -------
        float. Information ratio.
    """
    diff_rets = returns - benchmark_returns
    diff_std = diff_rets.std()

    if np.isnan(diff_std) or diff_std == 0:
        return 0.0

    return diff_rets.mean() / diff_std

def calc_treynor_ratio(portf_returns, riskfree_returns, beta):
    """
    Risk-adjusted return where the adjustment is made ito the portfolio beta and not the 
    standard deviation as in the Sharpe Ratio    
    
    TR = (p - rf / beta)
    
    Parameters
    ----------
    
    Returns
    -------
    """
    
    if tolerant_equals(beta, 0):
        return np.nan

    return (portf_returns - riskfree_returns) / beta

# Risk Metrics
def calc_tracking_error(portf_returns, benchmark_returns):
    '''
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    
    relative_returns = portf_returns - benchmark_returns
    tracking_error = relative_returns.std(ddof=1)
    
    if (tolerant_equals(tracking_error, 0) or np.isnan(tracking_error)):
        return 0.0
        
    return tracking_error
    
def calc_max_drawdown(prices):
    """
    Calculates the max drawdown of a price series. If you want the
    actual drawdown series, please use to_drawdown_series.
    """
    return (prices / pd.expanding_max(prices)).min() - 1

def drawdown_details(drawdown):
    """
    Returns a data frame with start, end, days (duration) and
    drawdown for each drawdown in a drawdown series.

    .. note::

        days are actual calendar days, not trading days

    Args:
        * drawdown (pandas.TimeSeries): A drawdown TimeSeries
            (can be obtained w/ drawdown(prices).
    Returns:
        * pandas.DataFrame -- A data frame with the following
            columns: start, end, days, drawdown.

    """
    is_zero = drawdown == 0
    # find start dates (first day where dd is non-zero after a zero)
    start = ~is_zero & is_zero.shift(1)
    start = list(start[start == True].index)  # NOQA

    # find end dates (first day where dd is 0 after non-zero)
    end = is_zero & (~is_zero).shift(1)
    end = list(end[end == True].index)  # NOQA

    if len(start) is 0:
        return None

    # drawdown has no end (end period in dd)
    if len(end) is 0:
        end.append(drawdown.index[-1])

    # if the first drawdown start is larger than the first drawdown end it
    # means the drawdown series begins in a drawdown and therefore we must add
    # the first index to the start series
    if start[0] > end[0]:
        start.insert(0, drawdown.index[0])

    # if the last start is greater than the end then we must add the last index
    # to the end series since the drawdown series must finish with a drawdown
    if start[-1] > end[-1]:
        end.append(drawdown.index[-1])

    result = pd.DataFrame(columns=('start', 'end', 'days', 'drawdown'),
                          index=range(0, len(start)))

    for i in range(0, len(start)):
        dd = drawdown[start[i]:end[i]].min()
        result.ix[i] = (start[i], end[i], (end[i] - start[i]).days, dd)

    return result
    
def calc_value_at_risk(portf_returns, confidence):
    """
    Parameters
    ----------
    
    
    Returns
    -------
    """
    
def calc_marginal_risk(security_returns, weights):
    '''
    The change in portfolio risk when the weight in an instrument changes,
    i.e. an asset’s marginal contribution to portfolio risk
    
    Parameters
    ----------
    security_returns : pandas.core.frame.DataFrame
        DataFrame of security returns
    
    weights : pandas.core.series.Series
        portfolio weights
        
    Returns
    -------
    
    
    '''

# Data transforms
def to_returns(prices):
    """
    Calculates the simple arithmetic returns of a price series.

    Formula is: (t1 / t0) - 1

    Args:
        * prices: Expects a price series

    """
    return prices / prices.shift(1) - 1


def to_log_returns(prices):
    """
    Calculates the log returns of a price series.

    Formula is: ln(p1/p0)

    Args:
        * prices: Expects a price series

    """
    return np.log(prices / prices.shift(1))


def rebase(prices, value=100):
    """
    Rebase all series to a given intial value.

    This makes comparing/plotting different series
    together easier.

    Args:
        * prices: Expects a price series
        * value (number): starting value for all series.

    """
    return prices / prices.ix[0] * value
    
def to_price_index(returns, start=100):
    """
    Returns a price index given a series of returns.

    Args:
        * returns: Expects a return series
        * start (number): Starting level

    Assumes arithmetic returns.

    Formula is: cumprod (1+r)
    """
    return (returns.replace(to_replace=np.nan, value=0) + 1).cumprod() * 100

def to_drawdown_series(prices):
    """
    Calculates the drawdown series.

    This returns a series representing a drawdown.
    When the price is at all time highs, the drawdown
    is 0. However, when prices are below high water marks,
    the drawdown series = current / hwm - 1

    The max drawdown can be obtained by simply calling .min()
    on the result (since the drawdown series is negative)

    Args:
        * prices (TimeSeries or DataFrame): Series of prices.

    """
    # make a copy so that we don't modify original data
    drawdown = prices.copy()

    # set initial hwm (copy to avoid issues w/ overwriting)
    hwm = drawdown.ix[0].copy()
    isdf = isinstance(drawdown, pd.DataFrame)

    for idx in drawdown.index:
        tmp = drawdown.ix[idx]
        if isdf:
            hwm[tmp > hwm] = tmp
        else:
            hwm = max(tmp, hwm)

        drawdown.ix[idx] = tmp / hwm - 1

    # first row is 0 by definition
    drawdown.ix[0] = 0
    return drawdown
    
def extend_pandas():
    """
    Extends pandas' PandasObject (Series, TimeSeries,
    DataFrame) with some functions defined in this file.

    This facilitates common functional composition used in quant
    finance.

    Ex:
        prices.to_returns().dropna().calc_clusters()
        (where prices would be a DataFrame)
    """
    PandasObject.to_returns = to_returns
    PandasObject.to_log_returns = to_log_returns
    PandasObject.to_price_index = to_price_index
    PandasObject.rebase = rebase
    PandasObject.to_drawdown_series = to_drawdown_series
    
    PandasObject.calc_max_drawdown = calc_max_drawdown
    PandasObject.calc_value_at_risk = calc_value_at_risk
    PandasObject.calc_tracking_error = calc_tracking_error
    
    PandasObject.calc_cagr = calc_cagr
    PandasObject.calc_total_return = calc_total_return
    PandasObject.calc_active_premium = calc_active_premium
    
    PandasObject.as_percent = utils.as_percent
    PandasObject.as_format = utils.as_format
    
    PandasObject.calc_information_ratio = calc_information_ratio
    PandasObject.calc_prob_mom = calc_prob_mom
    PandasObject.calc_risk_return_ratio = calc_risk_return_ratio
    PandasObject.calc_sharpe_ratio = calc_sharpe_ratio
    PandasObject.calc_sortino_ratio = calc_sortino_ratio
    PandasObject.calc_treynor_ratio = calc_treynor_ratio
