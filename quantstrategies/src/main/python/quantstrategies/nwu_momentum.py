# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:22:03 2015

@author: Niel Swart
"""

from os import path, listdir, makedirs
import pandas as pd
import numpy as np

import datetime as dt
import datamanager.datamodel as dm
from datamanager.datamodel import MarketData
from core.envs import *
from quantstrategies.filters import greater_than_filter, less_than_filter, top_filter

def calc_means(data, fields, period = '1M'):
    
    means = {}
    for f in fields:
        data[f].fillna(method = 'pad', inplace=True)
        means[f] = data[f].last(period).mean()
        
        if type(means[f]) != pd.Series:
            raise TypeError
        
    return means

class NWUMomentum():
    """
    """
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

    def __init__(self, start_date, end_date):
        '''
        '''
        self.start_date = '2014-06-01'
        self.end_date = '2015-05-31'
        
        # Import the last 12 month's data
        self.data = MarketData.load_from_file(daily_path, fields, start_date, end_date)

        self.means = calc_means(self.data, fields)

    def filter_universe(self, listed):
        '''
        Apply filters
        '''

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

    def calc_momentum():
        '''
        Calculate momentum
        '''
        filtered = filter_universe(listed)
        fc = self.data['Close'][filtered].sort(ascending=False)

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

    def save(self):
        self.calc_momentum().to_excel(path.join('C:\\', 'Users', 'Niel', 'Google Drive', 'NWU', 'Portfolio', 'Portfolio_' + str(dt.date.today()) + '.xlsx'))