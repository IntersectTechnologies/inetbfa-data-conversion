# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 12:40:38 2014

@author: Niel

Data preprocessing script

- Change the format of the downloaded data
- 
"""

import preprocessing as prep

from os import path, listdir
from initialize import data
import pandas as pd
from fields import ratios, index_fields

#%%
## Ratios preprocessing starts here
import ratios_preprocessing as rp

downloads = path.join(data,'downloads','jse','ratios')
temp = path.join(data, 'temp','ratios')
processed = path.join(data, 'processed','ratios')

# source folders
listed_ratios = path.join(downloads, 'listed','csv')
delisted_ratios = path.join(downloads, 'delisted','csv')

prep.process_downloads(listed_ratios, path.join(temp , 'listed'))
#process_downloads(delisted_ratios, temp + 'delisted/')

merged = rp.merge_files(path.join(temp, 'listed'))

rp.extract_fields_and_save(merged, ratios, processed)

# Resample Ratios


#%%
import index_preprocessing as ip
# Process index data

downloads = path.join(data,'downloads','jse','indices', 'csv')
temp = path.join(data, 'temp','indices')
processed = path.join(data, 'processed','indices')            

prep.process_downloads(downloads, temp)
merged = ip.merge_files(temp)

ip.extract_fields_and_save(merged, index_fields, processed)

#%%

# Dividend Preprocessing

import dividend_preprocessing as dp
from utils import empty_clone

source = path.join(data, 'downloads', 'jse', 'dividends')
fns = listdir(source)
div_items, no_data, div_panel = dp.extract_dividends(source, fns)

daily_market = path.join(data, 'processed', 'market', 'daily', 'Close.csv')
close = pd.read_csv(daily_market, sep=',', index_col = 0, parse_dates=True)

zero = empty_clone(close)

dp.process_dividend_panel(div_panel,  path.join(data, 'processed', 'dividends', 'daily'), zero)