"""
Created on Thu Jun 04 21:06:13 2015

@author: Niel
"""

import pandas as pd
import datetime as dt
from os import path

from datamanager.datamodel import MarketData, DataModel
import datamanager.datamodel as dm
from datamanager.envs import *
from datamanager.load import get_equities

def calc_divmult(div, close):
    '''
    params:
    div - dividends of a single ticker [DataFrame]
    close - close of a single ticker
    '''

    assert type(div)==pd.DataFrame 
    assert type(close)==pd.DataFrame

    # calculate multiplier for each dividend payment
    mult = (1-(div/close)).dropna()
    mult = mult.sort_index(ascending=False)

    return mult

def backwards_calc(mult):
    '''
    Backwards calculate multipliers:
    div 10: Mult10 = (1- div/price)
    div 9 : Mult9 = (1-div/price)*Mult10
    etc

    return bmult
    '''

    bmult = {}
    # 
    for i, m in enumerate(mult):
        if c == 0:
            bmult[i] = m
        else:
            bmult[i] = m*mult[i-1]

    return bmult

def calc_adj_close(cp, dp):

    # Import closing price data with pandas
    close = pd.read_csv(cp, index_col = 0, parse_dates=True)

    # Import dividend ex date data with pandas
    divs = pd.read_csv(dp, index_col = 0, parse_dates=True)

    # fillna with pad.
    divmult = {}
    for t in divs.columns:
        # get the dividends and close of a single ticker and drop all NaN values
        tmp_div = divs[t].dropna()
        tmp_close = close[t].dropna()
    
        tmp_mult = calc_divmult(tmp_div, tmp_close)
        mult = backwards_calc(tmp_mult)
        divmult[t] = pd.Series(mult.values(), tmp_mult.index)

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
    

