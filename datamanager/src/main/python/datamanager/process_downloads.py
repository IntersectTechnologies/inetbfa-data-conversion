# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 15:19:35 2015

@author: Niel
"""

import pandas as pd
import numpy as np
from os import path, listdir
import datetime as dt

from datamodel import Equity
from core.envs import *

class Processor(object):
    '''
    '''
    
    @staticmethod
    def blank_ts_df(equities):
        startdate = pd.datetime(1990, 1 , 1).date()
        enddate = pd.datetime.today().date()
        cal = pd.bdate_range(startdate, enddate)
        
        # trading days - rows
        rows = cal
        
        # all equities - columns
        cols = equities.index
        
        # create new blank data frame
        dat = np.empty((len(rows), len(cols)))
        dat[:] = np.NAN
        
        template = pd.DataFrame(dat, index = rows, columns = cols)
        return template

class ReferenceProcessor(object):
    '''
    '''
    
    def __init__(self):
        '''
        '''
        
        self.fields = ['Industry',
                       'ISIN',
                       'Sector',
                       'Market Data Currency',
                       'Financial Currency',
                       'Ticker',
                       'Listing Status']
         
        self.fieldmap = [('industry', 'Industry', lambda x: (x.strip().split(' - ')[1] if x != 'Unclassified' else 'Unclassified') if (type(x) == unicode or type(x) == str) else 'Unclassified'),
                     ('isin', 'ISIN', lambda x: x.strip() if type(x) == unicode or type(x) == str else x),
                     ('sector', 'Sector', lambda x: (x.strip().split(' - ')[1] if x != 'Unclassified' else 'Unclassified') if (type(x) == unicode or type(x) == str) else 'Unclassified'),
                     ('marketdata_currency', 'Market Data Currency', lambda x: x.strip() if type(x) == unicode or type(x) == str else x),
                     ('financial_currency','Financial Currency', lambda x: x.strip() if (type(x) == unicode or type(x) == str) else x),
                     ('listing_status', 'Listing Status', lambda x: ('CURRENT' if x.strip() == 'Current' else x.strip()) if (type(x) == unicode or type(x) == str) else x),
                     ('fullname', 'Name', lambda x: x.strip() if type(x) == unicode or type(x) == str else x)]
        
    def load_new(self, fpath):
        '''
        '''
        drop_cols = [0, 1]
        drop_rows = [0, 1]
        
        if path.isfile(path.join(fpath, 'Reference.xlsx')):
            
            fn = path.join(fpath, 'Reference.xlsx')
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

    def update(self, old, new):
        
        upd = old.copy()
        
        for i in new.index:
            for f1, f2, func in self.fieldmap:  
                new_val = new[f2][i]
                cur_val = upd[f1][i]
                conv_val = func(new_val)
                if i in upd.index:
                    # update
                    if (type(cur_val) == unicode or type(cur_val) == str):
                        if conv_val != cur_val:
                            if conv_val != 'Unclassified': 
                                upd.set_value(i, f1, conv_val)   
                            elif conv_val == 'Unclassified' and cur_val == '':
                                upd.set_value(i, f1, conv_val) 
                else:
                    upd.set_value(i, f1, conv_val)
                    
            upd.set_value(i, 'last_update', str(dt.date.today()))
            
        return upd
        
class Validate(object):
    '''
    
    '''

class ErrorChecking(object):
    '''
    '''
    
    

class MarketDataProcessor(object):
    
    def __init__(self, reference):
        '''
        '''

        self.reference = reference
        
    def load_new(self, field, fpath):
        '''
        '''
        files = listdir(fpath)
        
        drop_cols = [0,1]
        drop_rows = 0
        
        if field in [f.split('.')[0] for f in files]:
            fn = path.join(fpath, field + '.xlsx')
            temp = pd.read_excel(fn, header=0, skiprows=[1, 2], index_col=2, parse_dates=True)                 
            temp.drop(temp.columns[drop_cols], axis=1, inplace=True)
            
            temp.drop(temp.index[drop_rows], axis=0, inplace=True)
            tickers = [t.split(':')[0] for t in temp.columns]
            temp.columns = tickers
            
            return temp
        
    def load_old(self, field, fpath):
        '''
        '''
        
        files = listdir(fpath)
        if field in [f.split('.')[0] for f in files]:
            fn = path.join(fpath, field + '.csv')
            temp = pd.read_csv(fn, header=0, index_col=0, parse_dates=True) 
            return temp
    
    def load_and_merge(self, field, old_fp, new_fp):
        '''
        '''
        old = self.load_old(field, old_fp)
        new = self.load_new(field, new_fp)
        return self.update(old, new)
        
    def save(self, data, dest_fpath):
        '''
        '''
        data.to_csv(dest_fpath)
    
    def update(self, olddata, newdata):
        '''
        '''
        
        blank = Processor.blank_ts_df(self.reference)
        
        blank.update(olddata)
        blank.update(newdata)
        
        return blank.copy()    
    