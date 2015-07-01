# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:55:49 2015

@author: Niel
"""

from os import path, listdir, makedirs
import sys
import pandas as pd
import datamodel as dm
from datamodel import MarketData
import numpy as np
import datetime as dt

from envs import *
from filters import *

daily_path = path.join(DATA_PATH, 'jse', 'equities', 'daily')

listed = dm.get_all_listed()

fields = [
'Close',
'Market Cap',
'PE',
'DY',
'Volume',
'Total Number Of Shares'
]

start_date = '2014-06-01'
end_date = '2015-05-31'

data = MarketData.load_from_file(daily_path, fields, '2014-05-01', '2015-04-30')

valid_ix = [ix for ix in listed if ix in data['Close'].columns and ix in data['Total Number Of Shares'].columns]

print 'Number of available shares to select from: ' + str(len(valid_ix))

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

def calc_momentum(fc, startperiod, endperiod):
    
    mom = np.log(fc.shift(-endperiod)) - np.log(fc.shift(-startperiod))
    latest_mom = mom.ix[0]
    
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

output = calc_momentum(fc)
output['DY'] = data['DY'][filtered].last('1D').ix[0]
output['PE'] = data['PE'][filtered].last('1D').ix[0]

# C:\root\OneDrive\Intersect Technologies\Intersect Invest\Products
output.to_excel(path.join('C:\\', 'root', 'OneDrive', 'Intersect Technologies', 'Intersect Invest', 'Products', 'Growth Portfolio - ' + str(dt.date.today()) + '.xlsx'))