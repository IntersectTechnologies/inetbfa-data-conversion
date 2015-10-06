"""
Created on Thu Jun 04 21:06:13 2015

@author: Niel
"""

import pandas as pd
from datamanager.datamodel import DataModel
from datamanager.load import get_equities

def calc_divmult(div, close):
    '''
    params:
    div - dividends of a single ticker : Seriess
    close - close of a single ticker : Series

    return : Series
    '''

    assert isinstance(div, pd.Series)
    assert isinstance(close, pd.Series)

    # calculate multiplier for each dividend payment
    mult = (1-(div/close)).dropna()
    mult = mult.sort_index(ascending=False)

    return mult

def backwards_calc(multiplier):
    '''
    Backwards calculate multipliers:
    div 10: Mult10 = (1- div/price)
    div 9 : Mult9 = (1-div/price)*Mult10
    etc

    return bmult: dict
    '''
    assert isinstance(multiplier, pd.Series)
    bmult = {}
    for i, mult in enumerate(multiplier):
        if i == 0:
            bmult[i] = mult
        else:
            bmult[i] = mult*multiplier[i-1]

    return bmult

def calc_adj_close(closepath, divpath):

    # Import closing price data with pandas
    close = pd.read_csv(closepath, index_col = 0, parse_dates=True)

    # Import dividend ex date data with pandas
    divs = pd.read_csv(divpath, index_col = 0, parse_dates=True)

    # fillna with pad.
    divmult = {}
    for ticker in divs.columns:
        # get the dividends and close of a single ticker and drop all NaN values
        tmp_div = divs[ticker].dropna()
        tmp_close = close[ticker].dropna()

        tmp_mult = calc_divmult(tmp_div, tmp_close)
        mult = backwards_calc(tmp_mult)
        divmult[ticker] = pd.Series(mult.values(), tmp_mult.index)

    startdate = pd.datetime(2000, 1 , 1).date()
    divm = DataModel.blank_ts_df(list(get_equities().index), startdate)

    # ensure the integrity of the dataframe stays -- simplify algo
    for k in divmult.keys():
        divm[k] = divmult[k]

        divm.set_value(divm.index[-1], k, 1.0)

    # fillna with pad
    dmult = divm.bfill()
    adj_close = close * dmult;

    # Save to file
    return adj_close
    

