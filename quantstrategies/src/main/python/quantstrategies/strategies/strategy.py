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
from quantstrategies.universe_selection import greater_than_filter, less_than_filter, top_filter
from quantstrategies.transforms import last_mean

import itertools

try:
    import builtins
except ImportError:
    import __builtin__ as builtins


class Chainable(object):
    def __init__(self, data, method=None):
        self.data = data
        self.method = method

    def __getattr__(self, name):
        try:
            method = getattr(self.data, name)
        except AttributeError:
            try:
                method = getattr(builtins, name)
            except AttributeError:
                method = getattr(itertools, name)

        return Chainable(self.data, method)

    def __call__(self, *args, **kwargs):
        try:
            return Chainable(list(self.method(self.data, *args, **kwargs)))
        except TypeError:
            return Chainable(list(self.method(args[0], self.data, **kwargs)))
'''
Use it like this:
chainable_list = Chainable([3, 1, 2, 0])
(chainable_list
    .chain([11,8,6,7,9,4,5])
    .sorted()
    .reversed()
    .ifilter(lambda x: x%2)
    .islice(3)
    .data)
>> [11, 9, 7]

'''
class Strategy():
    """
    """
    def __init__(self, data):
        '''
        '''
        self.data = load_data(start_date, end_date);
        self.transforms = [] 
        self.listed = load_universe()


    @staticmethod
    def load_data(start_date = '2014-06-01', end_date = '2015-05-31'):
     
        daily_path = path.join(DATA_PATH, 'jse', 'equities', 'daily')
        fields = [
            'Close',
            'Market Cap',
            'Volume',
            'Total Number Of Shares',
            'VWAP'
        ]
        # Import the last 12 month's data
        return MarketData.load_from_file(daily_path, fields, start_date, end_date)
    
    @staticmethod
    def load_universe():
        '''
        '''

        listed = dm.get_all_listed()

    def universe_selection(self, filters):
        '''
        '''

        self.universe = load_universe()

    def transform(self, transforms, fields):
        '''
        transform_funcs - dict of name, func
        fields - dict of transform name and fields

        self.data - dict of dataframes
        '''
        for name, func in transforms:
            for f in fields[name]:
                self.transforms[name][f] = func(self.data[f])

    def security_selection(self, algo):
        '''
        Security selection
        '''

        return algo(data)

    def portfolio_selection(self, algo, data):
        '''

        :returns pandas series - keys ticker, values weights

        '''

        return algo(data);


    def run(self):
        
        self.universe_selection()
        self.transform()
        self.security_selection()
        self.portfolio_selection()

def generate_report(portfolio, cols, data):
        '''
        Calculate momentum
        '''

        # Select Universe
        refdata = dm.get_equities()

        output = refdata[cols].ix[portfolio.index].copy()
        output['Price'] = data['Close']
        return(output)

def save(report, filepath):
    report.to_excel(filepath + '.xlsx')

def get_data(data, portfolio, fields, date):
    '''
    '''