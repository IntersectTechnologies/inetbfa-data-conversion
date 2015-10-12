# Copyright 2015 Intersect Technologies CC
# 

from functools import partial
from datamanager.envs import *
from datamanager.load import get_equities
from quantstrategies.universe_selection import liquid_jse_shares
from quantstrategies.transforms import log_returns, index_log_returns, movavg, max
from quantstrategies.filters import apply_filter
import pandas as pd

def fields():
    return  [
        'Close',
        'Market Cap',
        'Volume',
        'Total Number Of Shares',
        'VWAP',
        'Adjusted Close'
    ]

def filter(data):
    '''
    Uses the Market Cap, Volume, Close, Total Number Of Shares to filter shares
    '''

    assert isinstance(data, dict)
    return(apply_filter(liquid_jse_shares, data))


def transform(data):
    '''
    Calculate the Detrended Oscillator
    '''

    assert isinstance(data, dict)

    fc = data['Adjusted Close'].sort(ascending=False)
    ma20 = partial(movavg, period=20)
    ma50 = partial(movavg, period=50)
    max20 = partial(max, period = 20)

    lr = log_returns(fc)
    ixlr = index_log_returns(lr)

    assert isinstance(ixlr.index, pd.DatetimeIndex)
    sma = ma20(ixlr)
    lma = ma50(ixlr)
    maximum = max20(ixlr)

    do = (sma - lma) / maximum
    out = data.copy()
    out['Detrended Oscillator'] = do
    return(out)

def security_selection(data):
    '''
    Select the top 15 securities based on momentum
    '''
    assert isinstance(data, dict)

    cols = [
        'fullname',
        'industry',
        'sector'
    ]

    equities = get_equities()
    output = equities[cols].ix[data['Close'].columns].copy()

    output['Detrended Oscillator'] = data['Detrended Oscillator']
    output['Price'] = data['Close'].last('1D').ix[0]
    return(output.sort(columns = 'Detrended Oscillator', ascending = False).ix[:15])

def portfolio_selection(data):
    '''
    '''
    assert isinstance(data, pd.DataFrame)
    return(data)