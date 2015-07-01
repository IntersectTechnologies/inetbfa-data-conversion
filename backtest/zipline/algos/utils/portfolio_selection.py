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

import numpy as np
import pandas as pd
import ffn

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