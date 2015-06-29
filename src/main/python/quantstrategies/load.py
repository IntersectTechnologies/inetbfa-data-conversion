# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 09:38:31 2015

@author: Niel
"""

import pandas as pd
from os import path
from os.path import expanduser

import pytz

DATA_PATH = path.join(
        expanduser("~"),
        '.zipline',
        'data'
        )

CACHE_PATH = path.join(
        expanduser("~"),
        '.zipline',
        'cache'
        )
    
def load_prices(tickers, start='2010-01-01', end=None):
    '''
    '''
    
    data = pd.read_csv(path.join(DATA_PATH, 'jse', 'market', 'daily', 'Close.csv'), sep = ',', index_col = 0, parse_dates = True)
    data = data.ix[start:end]
    
    return data[tickers].dropna()

def load_panel(data_metrics):
    '''
    
    Parameters
    ----------
    data_metrics : 
    
    Returns
    -------
    panel : 
    
    '''
    
    assert (type(data_metrics)== str or type(data_metrics==list))
    
    
    market_fp = path.join(DATA_PATH, 'jse', 'market', 'daily')
    dd = {}     # data dictionary
    
    for metric in data_metrics:   
        fp = path.join(market_fp, metric + '.csv')
        if path.exists(fp):
        
            stkd = pd.DataFrame.from_csv(fp)
            dd[metric] = stkd
        else: 	
            print 'Oops..'

    panel = pd.Panel(dd)
    panel.major_axis = panel.major_axis.tz_localize(pytz.utc)
    
    # Swap panel axes
    panel = panel.swapaxes(0, 2)
    return panel
  
def load_numtrades():
    '''
    
    '''
    
    return pd.read_csv(path.join(DATA_PATH, 'jse', 'market', 'daily', 'Number Of Trades.csv'), sep = ',', index_col = 0)

def load_totalnumshares():
    '''
    
    '''
    
    return pd.read_csv(path.join(DATA_PATH, 'jse', 'market', 'daily', 'Total Number Of Shares.csv'), sep = ',', index_col = 0, parse_dates=True)

def load_volume():
    '''
    '''
    
    return pd.read_csv(path.join(DATA_PATH, 'jse', 'market', 'daily', 'Volume.csv'), sep = ',', index_col = 0, parse_dates=True)
    
    
def load_marketcap():
    '''
    '''
    
    return pd.read_csv(path.join(DATA_PATH, 'jse', 'market', 'daily', 'Market Cap.csv'), sep = ',', index_col = 0, parse_dates=True)
    
def load_equities():
    '''
    '''
    
    EQUITIES = pd.read_csv(path.join(DATA_PATH, 'jse_equities.csv'), sep = ',', index_col = 0)
    
    return EQUITIES