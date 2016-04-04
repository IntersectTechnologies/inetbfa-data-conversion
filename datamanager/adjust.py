"""
Created on Thu Jun 04 21:06:13 2015

@author: Niel
"""

import pandas as pd
from datamanager.load import empty_dataframe

def __backwards_calc__(multiplier):
    '''
    Backwards calculate multipliers:
    div 10: Mult10 = (1- div/price)
    div 9 : Mult9 = (1-div/price)*Mult10
    etc

    return bmult: Series
    '''
    assert isinstance(multiplier, pd.Series)
    # sort from newest to oldest
    multiplier = multiplier.sort_index(ascending=False)    
    # make a copy of the multiplier Series
    mult = multiplier.copy()
    for i, multi in enumerate(multiplier):
        if i == 0:
            mult[i] = multi
        else:
            mult[i] = multi*mult[i-1]

    return mult

def calc_dividend_multiplier(div, close):
    '''
    params:
    div - dividends of a single ticker : Seriess
    close - close of a single ticker : Series

    return : Series
    '''

    assert isinstance(div, pd.Series)
    assert isinstance(close, pd.Series)

    # calculate multiplier for each dividend payment and remove all the NaN to ease calculation
    mult = (1-(div/close)).dropna()
    return __backwards_calc__(mult)

def calc_adj_close(close, divs, equities, enddate = None):
    '''
    Calculate the adjusted close
    '''

    # fillna with pad.
    divmult = empty_dataframe(equities, enddate=enddate)
    for ticker in divs.columns:
        # get the dividends and close of a single ticker and drop all NaN values
        tmp_div = divs[ticker].dropna()
        tmp_close = close[ticker].dropna()
        
        # now calculate the dividend multiplier for each ticker
        tmp_mult = calc_dividend_multiplier(tmp_div, tmp_close)
        divmult[ticker] = tmp_mult

    # get the new index 
    startdate = pd.datetime(2000, 1, 1).date()
    divm = empty_dataframe(equities, startdate, enddate=enddate)

    # update the blank dataframe - expand to the actual index
    divm.update(divmult) 
    # fillna with pad
    divm = divm.bfill()
    divm = divm.fillna(1)
    adj_close = close * divm

    # Save to file
    return adj_close
    
