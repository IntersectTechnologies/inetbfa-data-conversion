# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:55:49 2015

@author: Niel
"""

from os import path, listdir, makedirs
import sys

import pandas as pd

from os.path import expanduser
import datamodel as dm
from datamodel import MarketData, Reference

code_path = path.join('C:\\', 'root', 'repos', 'code')
sys.path.append(code_path)


DATA_PATH = path.join(
    expanduser("~"),
    '.zipline',
    'data'
)

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

data = MarketData.load_from_file(daily_path, fields, '2014-05-01', '2015-04-30')

valid_ix = [ix for ix in listed if ix in data['Close'].columns and ix in data['Total Number Of Shares'].columns]

print 'Number of available shares to select from: ' + str(len(valid_ix))


def calc_means(data, fields, '1M'):
    
    listed_mc = marketcap[valid_ix].last('1M')
    listed_mc.fillna(method = 'pad', inplace=True)
    mean_mc = listed_mc.mean()
    
    listed_pe = pe[valid_ix].last('1M')
    listed_pe.fillna(method = 'pad', inplace=True)
    mean_pe = listed_pe.mean()
    
    listed_dy = dy[valid_ix].last('1M')
    listed_dy.fillna(method = 'pad', inplace=True)
    mean_dy = listed_dy.mean()
    
    listed_vol = vol[valid_ix].last('2M')
    listed_vol.fillna(method = 'pad', inplace=True)
    mean_vol = listed_vol.mean()
    
    listed_si = si[valid_ix].last('2M')
    listed_si.fillna(method = 'pad', inplace=True)
    mean_si = listed_si.mean()

