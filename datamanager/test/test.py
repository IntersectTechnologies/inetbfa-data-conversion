# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 13:15:21 2015

@author: Niel
"""

from process_downloads import Processor, MarketDataProcessor, ReferenceProcessor, DividendProcessor
from datamodel import MarketData, Reference, Dividends
from os import path
from os.path import expanduser
import datetime as dt

DL_PATH = path.join('C:\\', 'root', 'data_downloads')

DATA_PATH = path.join(
    expanduser("~"),
    '.zipline',
    'data'
)

ref = Reference()

##
refp = ReferenceProcessor()
refnew = refp.load_new(DL_PATH)

refupd = refp.update(ref, refnew)
data = refupd.to_dataframe()
data = refupd.update_listing_status()

data.to_csv(path.join(DATA_PATH, 'latest_updates', 'jse_equities.csv'), sep=',', index=False)

##
prc = MarketDataProcessor(ref)

md = MarketData()
merged = prc.load_and_merge('Close', md.filepath, DL_PATH)

divp = DividendProcessor(ref)
divs = divp.load_new(DL_PATH, 'Dividend Ex Date')

#

blank = Processor.blank_ts_df(ref)
divs = Dividends.load_from_file(path.join(DATA_PATH, 'jse', 'equities', 'daily'), 'Dividend Ex Date')

divs = blank.update(divs)
close = MarketData.load_from_file(path.join(DATA_PATH, 'jse', 'equities', 'daily'), 'Close')

close.dropna(how='all')
mult = 1-(divs/close)