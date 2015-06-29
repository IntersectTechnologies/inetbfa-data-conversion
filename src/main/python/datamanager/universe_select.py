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
Created on Mon Dec 08 16:08:10 2014

@author: Niel
"""

import pandas as pd
from . import liquidity_metrics as lf 

def _get_larger_than(data, value, date='latest'):
    
    if type(date) == str and date=='latest':
        if type(data) == pd.DataFrame:
            d = data[-1].copy()
        else:
            assert type(data) == pd.Series
            d = data.copy()
    else:
        assert type(data) == pd.DataFrame
        assert type(date) == pd.Timestamp
        
        d = data.ix[date].copy()
    
    return d[d > value].index

def get_largest_price(pricedata, n, date='latest'):
    """
    Get the n equities with the largest nominal closing price

    Parameters
    ----------    
    pricedata : pandas.core.series.Series or DataFrame
    
    n : int

    date : string or pandas Timestamp    
    
    Returns
    -------
    """
    
    if type(date) == str:
        pass
    else:
        assert type(date) == pd.Timestamp
        
    
def get_larger_than_price(pricedata, price, date='latest'):
    """
    Get all equities with a nominal closing price larger than price
    
    Parameters
    ----------
    pricedata : pandas.core.series.Series or DataFrame
    
    Returns
    -------
    
    Index 
    """
    
    return _get_larger_than(pricedata, price, date)

def get_largest_marketcap(marketcap, n, date='latest'):
    '''
    Get the largest n equities by market cap 
    
    Parameters
    -----------
    n : int
    
    marketcapdata : pandas.core.series.Series
    
    Returns
    -------
    
    '''
    
    if type(date) == str:
        pass
    else:
        assert type(date) == pd.Timestamp    
    
    mc = marketcap.copy()
    mc.sort(ascending=False, na_position='last')
     
    return mc[:n].index

def get_larger_than_marketcap(marketcapdata, marketcap_threshold, date='latest'):
    '''
    Get all equities with a larger than specified market cap at the specified date (optional) 
    
    Parameters
    -----------
    n : int
    
    marketcapdata : pandas.core.series.Series
    
    marketcap_threshold : int or float
    
    date : str or pandas Timestamp
        Default 'latest'
        The specific date at which the market cap should be evaluated.  
        Only valid if marketcapdata is a DataFrame type
    
    Returns
    -------
    
    '''
    
    return _get_larger_than(marketcapdata, marketcap_threshold, date)

def get_larger_than_average_daily_volume(volumedata, volume_threshold, date='latest'):
    '''
    Parameters
    ----------
    volumedata : 
    
    volume_threshold :
    
    date : 
    
    Returns
    -------
    '''
    
    return _get_larger_than(volumedata, volume_threshold, date)
    
    
def min_fraction_of_trading_days(volume, minfraction):
    '''
    
    Parameters
    ----------
    
    volume - 
    
    minfraction - 
    
    Returns
    -------
    
    '''
    
    frac = lf.fraction_of_trading_days(volume)
    
    return frac[frac > minfraction].index
    
def get_most_liquid(n, volume, total_num_shares, numtrades, date='latest'):
    '''
    Get the n most liquid shares at a specific date
    
    liquidity - Average daily volume of shares traded as a percentage of total issued shares 
    for the last month multiplied by the average number of trades per day for the last month (21 days)
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    
    if type(date) == str:
        pass
    else:
        assert type(date) == pd.Timestamp
    
    offset =pd.DateOffset(-21)
    start = date + offset
    end = date
    
    lf.liquidity_score()
    score = lf.liquidity_score(volume, total_num_shares, numtrades)
    score.sort(ascending=False, na_position='last')
    
    return score[:n].index
    
def get_all(equities):
    '''
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    
    return equities.index
    
    
# TODO:    
def get_by_sector(equities, sector):
    '''
    
    Parameters
    ----------
    
    Returns
    -------
    '''    
    
def get_prefs(equities):
    '''
    Get all preference shares
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    
    eq = equities[equities.sharetype=='PREFERENCE'].copy()
    return eq.index
    
def get_ordinaries(equities):
    '''
    Get all ordinary shares
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    eq = equities[equities.sharetype=='ORDINARY'].copy()
    return eq.index
    
def get_all_listed(equities):
    '''
    Get all listed equities
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    eq = equities[equities.listing_status=='LISTED'].copy()
    return eq.index
    
    
def get_all_delisted(equities):
    '''
    Get all delisted equities
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    eq = equities[equities.listing_status=='DELISTED'].copy()
    return eq.index
    
    
def get_all_active(equities):
    '''
    Get all actively traded equities
    
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    eq = equities[equities.trading_status=='DELISTED'].copy()
    return eq.index
    
    
def get_all_suspended(equities):
    '''
    Get all suspended equities
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    
    eq = equities[equities.trading_status=='DELISTED'].copy()
    return eq.index