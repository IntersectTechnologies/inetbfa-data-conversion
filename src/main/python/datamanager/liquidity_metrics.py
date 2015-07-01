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
Created on Tue Jan 20 09:18:51 2015


@author: Niel
"""

import pandas as pd

def daily_ave_vol_month(montlhly_vol):
	'''
	Calculate the daily average volume over the last month
	'''
 
     
	
def daily_ave_vol_week(weekly_vol):
	'''
	Calculate the daily average volume over the last week
	'''
	
def sd_ave_vol(monthly_vol):
	'''
	Calculate the standard deviation of daily volume over the last month
	'''
 
def liquidity_score(volume, total_num_shares, numtrades):
    '''
    Calculate the liquidity score defined as:
    
    liquidity Score = Average daily volume of shares traded as a percentage of total issued shares 
    for the last month multiplied by the average number of trades per day for the last month (21 days)
    
    Parameters
    ----------
    volume : pandas dataframe
        Contains the volume history for all equities
    total_num_shares : pandas dataframe
        Contains the Total Number Of Shares issued history for all equities
    numtrades : pandas dataframe
        Contains the Number Of Trades history for all equities
        
    '''
    
    vol = volume.ix[-21:].copy()
    tns = total_num_shares.ix[-21:].copy()
    # remove those shares with no data for Total Number Of Shares
    mean_tns = tns.mean()    
    score1 = (vol.mean()/mean_tns[mean_tns > 0])*100
    
    numt = numtrades.ix[:-21].copy()
    score2 = numt.mean()   
    
    score = score1*score2
    
    return score

def fraction_of_trading_days(volume):
    '''
    
    Parameters
    ----------
    volume : pandas.core.frame.DataFrame    
    
    Returns
    -------
    
    fraction : pandas.core.series.Series
        Fraction of trading days for each security in volume
    
    '''
    
    assert volume == pd.DataFrame  
    
    numdays = len(volume.index)
    numtradingdays = len(volume[volume > 0])
    
    return numtradingdays / numdays

def trading_regularity_score(volume, numtrades):
    '''
    
    
    Parameters
    ----------
    volume : pandas.core.frame.DataFrame    
    
    numtrades : pandas.core.frame.DataFrame    
    
    Returns
    -------
    score : pandas.core.series.Series
    
    '''
    
    assert volume == pd.DataFrame
    assert numtrades == pd.DataFrame   
    
    return fraction_of_trading_days(volume) * numtrades.mean()