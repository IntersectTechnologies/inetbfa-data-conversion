# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 09:38:31 2015

@author: Niel
"""

import pandas as pd
from os import path
from datamanager.envs import DATA_PATH, MASTER_DATA_PATH
from datetime import datetime as dt

# globals
EQUITIES = pd.read_csv(path.join(DATA_PATH, 'jse', 'jse_equities.csv'), sep = ',', index_col = 0)
jse_path = path.join(DATA_PATH, 'jse')
daily_path = path.join(jse_path, 'equities', 'daily')

def load_close(tickers=None, start='2010-01-01', end=str(dt.today().date())):
    '''
    '''
    
    return load_field(field = 'Close', tickers=tickers, start=start, end = end)

def load_field(field = 'Close', tickers=None, start='2010-01-01', end=str(dt.today().date())):
    '''
    '''
    
    data = pd.read_csv(path.join(daily_path, field + '.csv'), sep = ',', index_col = 0, parse_dates = True)
    data = data.ix[start:end]
    
    if (tickers==None):
        return data.dropna(how='all')
    else:
        return data[tickers].dropna(how='all')

def load_fields(fields, tickers=None, start='2010-01-01', end=str(dt.today().date())):
    '''
    '''
    
    assert type(fields) == list
    data = {}
    for f in fields:
        temp = pd.read_csv(path.join(daily_path, f + '.csv'), sep=',', header=0, 
                    index_col=0, parse_dates=True)
                           
        temp = temp.ix[start:end]  
        
        if (tickers==None):
            temp = temp.dropna(how='all')
        else:
            temp = temp[tickers].dropna(how='all')

        temp.fillna(method = 'pad', inplace=True)
        data[f] = temp
        
    return data 
    
def load_panel(fields = ['Close']):
    '''
    
    Parameters
    ----------
    data_metrics : 
    
    Returns
    -------
    panel : 
    
    '''
    
    assert (type(data_metrics)== str or type(data_metrics==list))
    
    dd = {}     # data dictionary
    
    for metric in fields:   
        fp = path.join(daily_path, metric + '.csv')
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
    
    return pd.read_csv(path.join(daily_path, 'Number Of Trades.csv'), sep = ',', index_col = 0)

def load_totalnumshares():
    '''
    
    '''
    
    return pd.read_csv(path.join(daily_path, 'Total Number Of Shares.csv'), sep = ',', index_col = 0, parse_dates=True)

def load_volume():
    '''
    '''
    
    return pd.read_csv(path.join(daily_path, 'Volume.csv'), sep = ',', index_col = 0, parse_dates=True)
       
def load_marketcap():
    '''
    '''
    
    return pd.read_csv(path.join(daily_path, 'Market Cap.csv'), sep = ',', index_col = 0, parse_dates=True)
    
def load_equities():
    '''
    '''
    
    EQUITIES = pd.read_csv(path.join(jse_path, 'jse_equities.csv'), sep = ',', index_col = 0)
    
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
