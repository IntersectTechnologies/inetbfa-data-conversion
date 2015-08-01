# Copyright 2015 Intersect Technologies CC
# Copyright 2014 Quantopian, Inc.
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
Created on Tue Feb 10 09:09:14 2015

@author: Niel
"""

import math
import numpy as np
import numpy.linalg as la
import ffn

def sharpe_ratio(portf_return, riskfree_return, portf_volatility):
    """
    http://en.wikipedia.org/wiki/Sharpe_ratio
    
    Parameters
    ----------
        algorithm_volatility (float): Algorithm volatility.
        algorithm_return (float): Algorithm return percentage.
        treasury_return (float): Treasury return percentage.

    Returns
    -------
        The Sharpe ratio (float) : 
    """
    if q_math.tolerant_equals(portf_volatility, 0):
        return np.nan

    return (portf_return - riskfree_return) / portf_volatility

def max_drawdown(portf_prices):
    """
    Parameters
    ----------
    
    
    Returns
    -------
    """
    
    return ffn.calc_max_drawdown(portf_prices)

def downside_risk(portf_returns, mean_returns, normalization_factor):
    """
    Parameters
    ----------
    
    
    Returns
    -------
    """
    
    
    rets = portf_returns.round(8)
    mar = mean_returns.round(8)
    mask = rets < mar
    downside_diff = rets[mask] - mar[mask]
    
    if len(downside_diff) <= 1:
        return 0.0
    return np.std(downside_diff, ddof=1) * math.sqrt(normalization_factor)


def sortino_ratio(portf_period_return, riskfree_period_return, mar):
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
    if q_math.tolerant_equals(mar, 0):
        return 0.0
    
    return (portf_period_return - riskfree_period_return) / mar

def tracking_error(portf_returns, benchmark_returns):
    '''
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    
    relative_returns = portf_returns - benchmark_returns
    tracking_error = relative_returns.std(ddof=1)
    
    if (q_math.tolerant_equals(tracking_error, 0) or np.isnan(tracking_error)):
        return 0.0
        
    return tracking_error
    
def active_premium(portf_returns, benchmark_returns):
    '''
    
    Parameters
    ----------
    
    Returns
    -------
    
    
    '''
    relative_returns = portf_returns - benchmark_returns
    return np.mean(relative_returns)

def information_ratio(portf_returns, benchmark_returns):
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
    relative_returns = portf_returns - benchmark_returns
    relative_deviation = relative_returns.std(ddof=1)

    if (q_math.tolerant_equals(relative_deviation, 0) or np.isnan(relative_deviation)):
        return 0.0

    return np.mean(relative_returns) / relative_deviation

def treynor_ratio(portf_returns, riskfree_returns, beta):
    """
    Risk-adjusted return where the adjustment is made ito the portfolio beta and not the 
    standard deviation as in the Sharpe Ratio    
    
    TR = (p - rf / beta)
    
    Parameters
    ----------
    
    Returns
    -------
    """
    
    if q_math.tolerant_equals(beta, 0):
        return np.nan

    return (portf_returns - riskfree_returns) / beta
    
def value_at_risk(portf_returns, confidence):
    """
    Parameters
    ----------
    
    
    Returns
    -------
    """
    
def marginal_risk(security_returns, weights):
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

def volatility(daily_returns, num_trading_days):
    '''
    
    Parameters
    ----------
    
    
    Returns
    -------
    '''
    return np.std(daily_returns, ddof=1) * math.sqrt(num_trading_days)
    
def return_distribution(portf_returns, secwurity_returns, weights):
    '''
    Parameters
    ----------
    
    
    Returns
    -------
    '''


def random_portfolio(security_returns, weights):
    '''
    Parameters
    ----------
    
    
    Returns
    -------
    '''
    

def alpha(portf_period_return, riskfree_period_return,
          benchmark_period_returns, beta):
    """
    http://en.wikipedia.org/wiki/Alpha_(investment)

    Parameters
    ----------
    algorithm_period_return : float
        Return percentage from algorithm period.
    riskfree_period_return : float
        Return percentage for treasury period.
    benchmark_period_return : float
        Return percentage for benchmark period.
    beta : float
        beta value for the same period as all other values

    Returns
    -------
    The alpha of the portfolio : float
    """
    
    return portf_period_return - \
        (riskfree_period_return + beta *
         (benchmark_period_returns - riskfree_period_return))

def beta(portfolio_returns, benchmark_returns):
    """

    .. math::

        \\beta_a = \\frac{\mathrm{Cov}(r_a,r_p)}{\mathrm{Var}(r_p)}

    http://en.wikipedia.org/wiki/Beta_(finance)
    
    Parameters
    ----------
    
    
    Returns
    -------
    """
    # it doesn't make much sense to calculate beta for less than two days,
    # so return none.
    if len(portfolio_returns) < 2:
        return 0.0, 0.0, 0.0, 0.0, []

    returns_matrix = np.vstack([portfolio_returns,
                                benchmark_returns])
    C = np.cov(returns_matrix, ddof=1)
    eigen_values = la.eigvals(C)
    condition_number = max(eigen_values) / min(eigen_values)
    algorithm_covariance = C[0][1]
    benchmark_variance = C[1][1]
    beta = algorithm_covariance / benchmark_variance

    return (
        beta,
        algorithm_covariance,
        benchmark_variance,
        condition_number,
        eigen_values
    )