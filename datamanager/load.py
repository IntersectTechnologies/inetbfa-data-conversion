# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 09:38:31 2015

@author: Niel
"""

import pandas as pd
from os import path
from datamanager.envs import MASTER_DATA_PATH
from datetime import datetime as dt

# globals
EQUITIES = pd.read_csv(path.join(MASTER_DATA_PATH, 'jse_equities.csv'), sep = ',', index_col = 0)
daily_path = MASTER_DATA_PATH

def marketdata_fields():
    return [
            'Close',
            'High',
            'Low',
            'Open',
            'DY',
            'EY',
            'Market Cap',
            'PE',
            'Total Number Of Shares',
            'Last Bid',
            'Last Offer',
            'Volume',
            'VWAP',
            'Book Value per Share',
            'Dividend Ex Date',
            'Dividend Declaration Date',
            'Dividend Payment Date'
        ]

def equity_ref_fields():
    '''
    Should be based on the actual data
    '''

    return [ 'ticker',        
            'isin',
            'shortname',
            'fullname',
            'industry',
            'supersector',
            'sector',
            'subsector',
            'listing_status',
            'listing_date',
            'trading_status',
            'equity_type',
            'equity_class',
            'marketdata_currency',
            'financial_currency',
            'last_update',
            'alsi_member',
            'top40_member',
            'irregular_flag'
        ]

def get_equity_ref_fields_from_files(dirpath):
    '''
    '''

def get_marketdata_fields_from_files(dirpath):
    '''
    '''



def get_all_equities_from_data(all_path, new_path, field):
    field_all = load_market_data(all_path, field)
    all = list(field_all.columns)
    field_current = load_market_data(new_path, field)
    current = list(field_current.columns)

    return equities_from_data(current, all)

def equities_from_data(current_list, all_list):
    '''
    '''

    all_set = set(all)
    current_set = set(current)

    delisted = all - current
    newly_listed = current - all

    new_all_set = all_set + current_set

    return(new_all_set, current_set, newly_listed, delisted)

def load_intebfa_ts_data(filepath):
    '''
    '''
    drop_cols = [0,1]
    drop_rows = 0
        
    temp = pd.read_excel(filepath, header=0, skiprows=[1, 2], index_col=2, parse_dates=True)                 
    temp.drop(temp.columns[drop_cols], axis=1, inplace=True)
            
    temp.drop(temp.index[drop_rows], axis=0, inplace=True)
    tickers = [t.split(':')[0] for t in temp.columns]
    temp.columns = tickers
        
    return temp.sort_index()

def load_inetbfa_ref_data(fpath):
    '''
    '''
    drop_cols = [0, 1]
    drop_rows = [0, 1]
        
    if path.isfile(fpath):
            
        fn = fpath
        temp = pd.read_excel(fn, header=0, skiprows=[2], index_col=2, parse_dates=True)                 
        temp.drop(temp.columns[drop_cols], axis=1, inplace=True)
        fields = [f for f in temp.ix[0]]
        names = [n.split('(')[0] for n in temp.ix[1]]
        tickers = [t.split(':')[0] for t in temp.columns]
        nd = {}
        for t, n in zip(tickers, names):
            nd[t] = n
        nds = pd.Series(nd)
            
        mindex = mindex = pd.MultiIndex.from_arrays([tickers, fields])
        temp.drop(temp.index[drop_rows], axis=0, inplace=True)
        temp.columns = mindex
            
        temp.dropna(how='all', inplace = True)
        temp = temp.ix[0].unstack()
            
        temp['Name'] = nds
        return temp

def load_ts(filepath):
    temp = pd.read_csv(fn, header=0, index_col=0, parse_dates=True) 
    return temp

def load_field_ts(fpath, field='Close', startdate='1990-01-01', enddate = None):
        '''
        '''
        
        if type(field) == str:
            temp = pd.read_csv(path.join(fpath, field + '.csv'), sep=',', header=0, 
                           index_col=0, parse_dates=True)
                           
            temp = temp.ix[startdate:enddate]               
            temp.fillna(method = 'pad', inplace=True)               
            data = temp
                           
        if type(field) == list:
            data = {}
            for f in field:
                temp = pd.read_csv(path.join(fpath, f + '.csv'), sep=',', header=0, 
                           index_col=0, parse_dates=True)
                           
                temp = temp.ix[startdate:enddate]  
                temp.fillna(method = 'pad', inplace=True)
                data[f] = temp
        
        return data

def load_market_data(fpath, field):
    '''
    load market data for a specific field from a csv file with name field
    Parameters
    ----------
    fpath : str
       the path of the file to load exculding the filename
    field : str
        the name and filename of the field to load

    Return
    --------
    data : pandas.DataFrame
        Returns a pandas dateframe with a time series index and the tickers as column headers
    '''
    data = pd.read_csv(path.join(fpath, field + '.csv'), sep = ',', index_col = 0, parse_dates=True)
    return data  

def empty_dataframe(equities,  startdate = pd.datetime(1990, 1 , 1).date(), enddate = None):
    '''
    Creates an empty dataframe with a time series index and a column index populated with the equities supplied

    Paramaters
    -------
    equities : list
        The equities to create the column index for

    startdate : date
        The start date of the time series index

    enddate : date
        The end date of the time series index

    Return
    ------
    data : pandas.DataFrame
        
    '''

    if enddate is None:
        enddate = pd.datetime.today().date()

    cal = pd.bdate_range(startdate, enddate)
        
    # trading days - rows
    rows = cal
        
    # all equities - columns
    cols = equities
        
    # create new blank data frame
    dat = np.empty((len(rows), len(cols)))
    dat[:] = np.NAN
        
    template = pd.DataFrame(dat, index = rows, columns = cols)
    return template

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
            print('Oops..')

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
    
    EQUITIES = pd.read_csv(path.join(daily_path, 'jse_equities.csv'), sep = ',', index_col = 0)
    
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
