# Copyright 2015 Intersect Technologies CC
# 

from functools import partial
from datamanager.envs import *
from quantstrategies.transforms import mean, momentum, log_returns, index_log_returns, movavg, max

def fields():
    return  [
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
    short_movavg = partial(movavg, period=20)
    long_movavg = partial(movavg, period=50)
    max20 = partial(max, period = 20)

    lr = log_returns(data)
    rets = returns(data)
    ixlr = index_log_returns(lr)

    ma20 = short_movavg(ixlr)
    ma50 = long_movavg(ixlr)
    mom = momentum(ixlr)
    mean = mean(ixlr)

    do = (ma20 - ma50) / max20

    return do

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
    output = equities[cols].ix[filtered].copy()

    output['Momentum - 12M'] = latest_mom
    output['Price'] = self.data['Close'].last('1D').ix[0]
    return(output.sort(columns = 'Momentum - 12M', ascending = False))

def portfolio_selection(data):
    '''
    '''