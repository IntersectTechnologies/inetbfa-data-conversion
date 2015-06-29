# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 21:06:13 2015

@author: Niel
"""

from envs import *
from os import path
from datamodel import MarketData, DataModel
import datamodel as dm
import pandas as pd
import datetime as dt

def calc_adj_close():

    # Import closing price data with pandas
    cp = path.join(DATA_PATH, "jse", "equities", "daily", "Close.csv")
    close = pd.read_csv(cp, index_col = 0, parse_dates=True)

    # Import dividend ex date data with pandas
    dp = path.join(DATA_PATH, "jse", "equities", "daily", "Dividend Ex Date.csv")
    divs = pd.read_csv(dp, index_col = 0, parse_dates=True)

    # Calculate multipliers for each dividend payment

    # fillna with pad.
    divmult = {}
    for t in divs.columns:
        tmp_div= divs[t].dropna()
        tmp_close = close[t].dropna()
    
        tmp_mult = (1-(tmp_div/tmp_close)).dropna()
        tmp_mult = tmp_mult.sort_index(ascending=False)
        mult = {}
        # Backwards calculate multipliers:
        # div 10: Mult10 = (1- div/price)
        # div 9 : Mult9 = (1-div/price)*Mult10
        # etc
        for c, i in enumerate(tmp_mult):
            if c == 0:
               mult[c] = i
            else:
               mult[c] = i*mult[c-1]

        divmult[t] = pd.Series(mult.values(), tmp_mult.index)

    startdate = pd.datetime(2000, 1 , 1).date()
    divm = DataModel.blank_ts_df(dm.get_all(), startdate)

    for k in divmult.iterkeys():
        divm[k] = divmult[k]
        divm.set_value(divm.index[-1], k, 1.0)

    # fillna with pad
    dmult = divm.bfill()
    adj_close = close * dmult;

    # Save to file

    return adj_close
    

