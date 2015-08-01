# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 13:12:18 2014

@author: Niel

Extract lineitem values from ratios

"""

from initialize import data
from os import path
import pandas as pd

source = path.join(data, 'processed', 'ratios')

book_value_ps = pd.read_csv(path.join(source, 'Book Value Per Share (c).csv'), sep = ',', index_col = 0, parse_dates=True)
price = pd.read_csv(path.join(source, 'Price Per Share (c).csv'), sep = ',', index_col = 0, parse_dates=True)
price2book = pd.read_csv(path.join(source, 'Price Per Book Value.csv'), sep = ',', index_col = 0, parse_dates=True)

p2b_self = price/book_value_ps
bookvalue_monthly = book_value_ps.resample('M', fill_method='pad')