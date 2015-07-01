# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 11:34:28 2015

@author: Niel
"""

from os import path
import pandas as pd
import numpy as np
import datetime as dt

from core.envs import *

EQUITIES = pd.read_csv(path.join(MASTER_DATA_PATH, 'jse', 'jse_equities.csv'), sep = ',', index_col = 0)

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
    
def update_listing_status():
    
    def update_ls(ls, lu, ix):
        if lu != str(dt.date.today()) and ls != 'DELISTED':
            EQUITIES.set_value(ix, 'listing_status', 'DELISTED')

    map(update_ls, EQUITIES['listing_status'], EQUITIES['last_update'], EQUITIES.index)    
    EQUITIES.to_csv(path.join(MASTER_DATA_PATH, 'jse', 'jse_equities.csv'), sep = ',', index_col = 0)
    return EQUITIES
        
class DataModel(object):
    
    def __init__(self):
        '''
        '''
        
        self.fields = []
    
    def load_from_file(fpath, field):
        '''
        '''
        data = pd.read_csv(path.join(fpath, field + '.csv'), sep = ',', index_col = 0, parse_dates=True)
        
        return data            
     
    @staticmethod
    def blank_ts_df(equities, startdate = pd.datetime(1990, 1 , 1).date(), enddate = None):
        
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
      
class Equity(DataModel):
    
    fields = [
            'ticker',        
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
        
    def __init__(self, ticker):
        self.exchange = 'JSE'
        
        self.id = ticker
        self.properties = {}
        
        for field in Equity.fields:
            self.properties[field] = None
            
        self.properties['ticker'] = ticker
        
    @staticmethod
    def create_from_relation(ticker, series):
        '''
        '''
        
        equity = Equity(ticker)
        
        for key, value in series.iteritems():
            
            if key in Equity.fields:
                if key == 'ticker' and ticker != value:
                    print 'Oops...'
                    break
                else:
                    equity.properties[key] = value
        
        return equity

class Equities(DataModel):
    
    
    def __init__():
        '''
        '''
        
        self.__dict = {}
    
    def to_dataframe(self):
        '''
        '''
        
        index = self.__dict.keys()
        columns = Equity.fields
        
        data = {}
        for field in Equity.fields:
            data[field] = []
            for key in self.__dict.keys():
                data[field].append(self.__dict[key].properties[field])
        
        for k in data.keys():
            data[k] = pd.Series(data[k], index=index)
            
        self.data = pd.DataFrame(data, index = index, columns=columns)
        
        return self.data
    
    def load_from_file(self):
        '''
        '''
        data = EQUITIES
        for i in data.index:
            self.__dict[i] = Equity.create_from_relation(i, data.ix[i])
           
class Dividends(DataModel):
    '''

    '''
    fields = [
            'Dividend Ex Date',
            'Dividend Declaration Date',
            'Dividend Payment Date'
        ]
        
    def __init__(self):
        '''
        '''
        
        self.fields = []
    
class Indices(DataModel):

    def __init__(self):
        '''
        '''
        
        self.fields = [
            'Close',
            'DY',
            'EY',
            'High',
            'Low',
            'Market Cap',
            'Market Cap Free Float',
            'Open',
            'PE',
            'TRI',
            'Volume'
        ]
        
        
class MarketData(DataModel):
    '''
    '''
    
    fields = [
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
            'Number Of Trades',
            'Volume',
            'VWAP'
        ]
        
    filepath = path.join(MASTER_DATA_PATH, 'jse', 'equities', 'daily')
    
    def __init__(self):
        '''
        '''

    @staticmethod
    def load_from_file(fpath, field='Close', startdate='1990-01-01', enddate = None):
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
            
    
class Ratios(DataModel):
    '''
    '''
    
    def __init__(self):
        
        self.fields = [
            'Book Value / Share (c)',
            'Cash Flow / Share (c)',
            'Debt / Assets',
            'Debt / Equity', 
            'NAV / Share (c)',
            'Earnings / Share (c)',
            'Earnings Yield %',
            'Dividend Yield %',
            'Dividend / Share (c)',
            'Price / Book Value',
            'Price / Cash',
            'Price / Cash Flow',
            'Net Profit Margin %',
            'Operating Profit Margin %',
            'Price / EBIT',
            'Price / Earnings',
            'Price / EBITDA',
            'Price / NAV',
            'Price / Share (c)',
            'Return On Equity %',
            'Dividend / Share',
            'Earnings / Share',
            'Enterprise Value',
            'Enterprise Value / Cash',
            'Enterprise Value / EBIT',
            'Enterprise Value / EBITDA',
            'Enterprise Value / PAT',
            'Enterprise Value / Share',
            'Total Assets',
            'Price / Share To Cash Flow / Share',
            'Return On Average Equity %',
            'Return On Assets %',
            'Return On Average Assets %',
            'Return On Capital Employed %'
        ]