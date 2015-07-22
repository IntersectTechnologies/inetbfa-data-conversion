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
from datamanager.envs import *
from quantstrategies.filters import greater_than_filter, less_than_filter, top_filter

class Strategy():
    """
    """

    def __init__(self, start_date, end_date):
        '''
        '''
        self.start_date = '2014-06-01'
        self.end_date = '2015-05-31'
        
        daily_path = path.join(DATA_PATH, 'jse', 'equities', 'daily')
        fields = [
            'Close',
            'Market Cap',
            'Volume',
            'Total Number Of Shares',
            'VWAP'
        ]
        # Import the last 12 month's data
        self.data = MarketData.load_from_file(daily_path, fields, start_date, end_date)

        self.means = calc_means(self.data, fields)

    def filter(self, listed):
        '''
        Apply filters
        '''

        filtered = listed

        
        return(filtered)

    def calc(self):
        
        '''
        Calculate momentum
        '''
        # Select Universe
        listed = dm.get_all_listed()
        filtered = self.filter_universe(listed)
           
        equities = dm.get_equities()

        cols = [
        'fullname',
        'industry',
        'sector'
        ]

        output = equities[cols].ix[filtered].copy()

        output['Price'] = self.data['Close'].last('1D').ix[0]
        # RANK
        return(output)

    def save(self, filepath):
        self.calc().to_excel(filepath + '.xlsx')