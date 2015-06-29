# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:22:03 2015

@author: Niel Swart
"""

from os import path, listdir, makedirs
import pandas as pd
import numpy as np

import datetime as dt
import datamodel as dm
from datamodel import MarketData
from envs import *

def calc_means(data, fields, period = '1M'):
    
    means = {}
    for f in fields:
        data[f].fillna(method = 'pad', inplace=True)
        means[f] = data[f].last(period).mean()
        
        if type(means[f]) != pd.Series:
            raise TypeError
        
    return means

def less_than_filter(data, threshold):
    return data[data < threshold].index
    
def greater_than_filter(data, threshold):
    return data[data >= threshold].index

def top_filter(data, n):
    data.sort(ascending = False)
    return data[0:n].index    


start_date = '2014-06-01'
end_date = '2015-05-31'

daily_path = path.join(DATA_PATH, 'jse', 'equities', 'daily')

# Select Universe
listed = dm.get_all_listed()

fields = [
    'Close',
    'Market Cap',
    'Volume',
    'Total Number Of Shares',
    'VWAP'
]

# Import the last 12 month's data
data = MarketData.load_from_file(daily_path, fields, start_date, end_date)

# CALCULATE MEANS
#################
means = calc_means(data, fields)

## APPLY FILTERS
################

def filter_universe(listed):
    
    filtered = listed

    # Volume zero filter
    filtered = filtered.intersection(greater_than_filter(means['Volume'], 1))

    # Price filter
    filtered = filtered.intersection(greater_than_filter(data['Close'].last('1D').ix[0], 100))
    
    # Market Cap filter
    filtered = filtered.intersection(top_filter(means['Market Cap'], 200))
    
    # Trading Frequency Filter
    filtered = filtered.intersection(greater_than_filter((means['Volume']/means['Total Number Of Shares'])*100, 0.01))
    
    return(filtered)

## CALCULATE MOMENTUM
#####################
filtered = filter_universe(listed)
fc = data['Close'][filtered].sort(ascending=False)

def calc_momentum(fc):
    
    mom12 = np.log(fc.shift(-21)) - np.log(fc.shift(-252))
    latest_mom = mom12.ix[0]
    
    equities = dm.get_equities()

    cols = [
    'fullname',
    'industry',
    'sector'
    ]

    output = equities[cols].ix[filtered].copy()

    output['Momentum - 12M'] = latest_mom
    output['Price'] = data['Close'].last('1D').ix[0]
    # RANK
    return(output.sort(columns = 'Momentum - 12M', ascending = False))

calc_momentum(fc).to_excel(path.join('C:\\', 'Users', 'Niel', 'Google Drive', 'NWU', 'Portfolio', 'Portfolio_' + str(dt.date.today()) + '.xlsx'))