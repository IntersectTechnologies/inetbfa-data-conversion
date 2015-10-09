# Copyright 2015 Intersect Technologies CC
# 
'''
Created on Sat May 23 15:22:03 2015
@author: Niel Swart
'''

import numpy as np
from datamanager.load import get_equities
from quantstrategies.universe_selection import liquid_jse_shares

def fields():
    return [
        'Close',
        'Market Cap',
        'Volume',
        'Total Number Of Shares',
        'VWAP'
    ]

def filter(data):
    '''
    Uses the Market Cap, Volume, Close, Total Number Of Shares to filter shares
    '''

    return(liquid_jse_shares(data))

def transform(data):
    '''
    Calculate the momentum
    '''
    fc = data['Close'].sort(ascending=False)
    mom12 = np.log(fc.shift(-21)) - np.log(fc.shift(-252))

    return mom12

def security_selection(data):
    '''
    Select the top 15 securities based on momentum
    '''
    
    latest_mom = data.ix[0]
    cols = [
        'fullname',
        'industry',
        'sector'
    ]

    equities = get_equities()
    output = equities[cols].ix[data.columns].copy()

    output['Momentum - 12M'] = latest_mom
    output['Price'] = data.last('1D').ix[0]
    return(output.sort(columns = 'Momentum - 12M', ascending = False))

def portfolio_selection(data):
    '''
    '''

    return(data.ix[:15])


