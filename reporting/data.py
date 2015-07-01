# -*- coding: utf-8 -*-
"""
Created on Sat Apr 05 20:16:58 2014

@author: nielswart
"""

def change_column_names(mapping, pricedata):
    '''
    change column names from name given by data provider to security ids used in mapping
    
    pricedata - pandas dataframe of all pricedata
    
    mapping - pandas dataframe of reference data on all securities
    '''
    
    oldcols = pricedata.columns
    
    names = [col.split(' - ') for col in oldcols]
    
    newcols = [mapping[mapping['ticker']==ticker and mapping['name']==name].index[0] for ticker, name in names]
    
def calc_returns(pricedata):
    '''
    
    '''
    
def fill_proxy_data(pricedata):
    '''
    
    '''

def convert_currency(mapping, pricedata, currency):
    '''
    
    '''
    
    