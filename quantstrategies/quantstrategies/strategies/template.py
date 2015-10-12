# Copyright 2015 Intersect Technologies CC
# 
'''
Created on Sat May 23 15:22:03 2015
@author: Niel Swart
'''

import numpy as np
import pandas as pd
from datamanager.load import get_equities
from quantstrategies.universe_selection import liquid_jse_shares
from quantstrategies.filters import apply_filter

def fields():
    return [

    ]

def filter(data):
    '''
    Uses the Market Cap, Volume, Close, Total Number Of Shares to filter shares
    '''
    assert isinstance(data, dict)

def transform(data):
    '''
    Calculate the momentum
    '''
    assert isinstance(data, dict)


    out = {}
    out = data.copy()
    
    return out

def security_selection(data):
    '''
    Select the top 15 securities based on momentum
    '''
    assert isinstance(data, dict)


    return(output.sort(columns = 'Momentum - 12M', ascending = False))

def portfolio_selection(data):
    '''
    '''

    assert isinstance(data, pd.DataFrame)
    return(data.ix[:15])


