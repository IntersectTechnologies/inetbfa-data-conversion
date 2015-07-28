# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 09:38:31 2015

@author: Niel
"""

import pandas as pd
from os import path
from os.path import expanduser
from datamanager.envs import DATA_PATH
import pytz

EQUITIES = pd.read_csv(path.join(MASTER_DATA_PATH, 'jse', 'jse_equities.csv'), sep = ',', index_col = 0)

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

def set_equities(equities):
    '''
    '''
    global EQUITIES
    if type(equities) == pd.DataFrame:
        EQUITIES = equities
    else:
        raise ValueError
    
def get_equities():
    '''
    '''
    
    eq = EQUITIES.copy()
    return eq
    
def get_all():
    '''
    '''        
    
    eq = EQUITIES.copy()
    return eq.index

def get_all_listed():
    '''
    Get all listed equities
    
    Returns
    -------

    Pandas DataFrame of all listed Equities
    '''
    
    eq = EQUITIES[EQUITIES.listing_status=='CURRENT'].copy()
    return eq.index 
    
def get_all_delisted():
    '''
    Get all delisted equities
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    eq = EQUITIES[EQUITIES.listing_status=='DELISTED'].copy()
    return eq.index
    
    
def get_all_active():
    '''
    Get all actively traded equities
    
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    eq = EQUITIES[EQUITIES.trading_status=='DELISTED'].copy()
    return eq.index
    
    
def get_all_suspended():
    '''
    Get all suspended equities
    
    Parameters
    ----------
    
    Returns
    -------
    '''
    
    eq = EQUITIES[EQUITIES.trading_status=='DELISTED'].copy()
    return eq.index    
 
# TODO: remove  
def update_listing_status():
    
    def update_ls(ls, lu, ix):
        if lu != str(dt.date.today()) and ls != 'DELISTED':
            EQUITIES.set_value(ix, 'listing_status', 'DELISTED')

    map(update_ls, EQUITIES['listing_status'], EQUITIES['last_update'], EQUITIES.index)    
    EQUITIES.to_csv(path.join(MASTER_DATA_PATH, 'jse', 'jse_equities.csv'), sep = ',', index_col = 0)
    return EQUITIES