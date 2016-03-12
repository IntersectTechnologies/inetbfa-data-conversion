import pandas as pd
import numpy as np
from functools import partial

'''
This module contains transformation functions for time series data based on pandas DataFrame's
'''

def detrended_oscillator(close):
    '''
    Calculate the detrended oscillator
    '''

    ma20 = partial(moving_avg, days=20)
    ma50 = partial(moving_avg, days=50)
    max20 = partial(max, period = 20)

    ixlr = index_log_returns(close)

    assert isinstance(ixlr.index, pd.DatetimeIndex)
    sma = ma20(ixlr)
    lma = ma50(ixlr)
    maximum = max20(ixlr)

    do = (sma - lma) / maximum
    
    return do

def resample_monthly(data, how = 'last'):
    '''
    Resample the data to a monthly frequency using a specific aggregation function
    '''
    data_monthly = data.resample('M', how = how)
    return data_monthly

def moving_avg(data, days, min_days = None):
    '''
    Calculate the moving average of the daily data

    Parameters
    ---------
    data : pandas.DataFrame

    days : int

    min_days : int

    Returns
    -----------
    '''

    return pd.rolling_mean(data, days, min_periods=min_days, freq='D')

def momentum_monthly(close, start_lag, end_lag):
    '''
    Calculate the momentum from monthly closing prices 
    
    Parameters
    -----
    close : pandas.DataFrame
        The closing prices to calculate the momentum from (columns are security identifiers and the index is a time series index)
        
    start_lag : int
        the starting month to calculate the momentum from relative to the newest (most recent) month in the data set (0). E.g. -12 is 12 months ago -1 is one month ago
    
    end_lag : int
        the ending month to calculate the momentum to relative to the most recent month.
    
    Returns 
    ----------
    momentum : pandas.DataFrame
        The price momentum
    
    '''
    
    assert close.index.freq == "M"
    
    # shift dates to align and calculate momentum
    mom = np.log(close.shift(end_lag)) - np.log(close.shift(start_lag))

    return mom
    
def earnings_momentum(ey, close, start_lag, end_lag):
    '''
    Calculate the momentum in the fundamental earnings of the company derived from the EY and the closing price
    '''
    
def pead_momentum(announcements, close):
    '''
    Calculate the price momentum from the most recent earnings announcement normalised to annualised returns
    A minimum of 2 days since the announcement (from day 3) is required. 
    
    Parameters
    -----------
    
    
    Returns
    -----------
    
    '''

    # make 1 at every earnings announcement
    anndays = announcements.applymap(lambda x: 0 if np.isnan(x) else 1)
    
    last_ann_price = close * anndays
    last_ann_price.ffill(inplace= True)
    days_since_df = last_ann_price.copy()

    # convert this to util function taking a predicate
    days_since = np.NaN
    for ticker in anndays.columns:
        for day in anndays.index:
            if (anndays.loc[day, ticker] == 1):
                days_since = 1
            else:
                days_since += 1
            
            days_since_df.loc[day, ticker] = days_since
  
    norm_factor = 252 / days_since_df
    # calculate returns
    norm_mom = (np.log(close) - np.log(last_ann_price)) * norm_factor

    return norm_mom

def earnings_surprise(announcements, close):
    '''
    Calculate the earnings surprise defined as the the cumulative return after a company earnings announcement for the days 0-2
    
    Returns
    -----
    surprise : pandas.DataFrame
        The cumulative return (surprise) values on the announcement days (index) - all NaN rows removed
    '''

    ea = announcements.dropna(how='all')
    # calculate the log returns
    logret = log_returns(close.drop_na(how='all'))

    # calculate the 3 day rolling sum of returns
    sum3day = pd.rolling_sum(logret.shift(-2), 3)

    # get the 3 day sum - the surprise
    ann = ea.applymap(lambda val: 0 if np.isnan(val) else 1)
    return ann * sum3day

def earnings_surprise_changes(announcements, close):
    '''
    Calculates the change in earnings suprises by comparing an earnings surprise to a previous surprise
    '''    

    # calculate the earnings surprise
    surprise = earnings_surprise(announcements, close)
    filled = surprise.ffill()

    diffd = filled.diff()


def earnings_surprise_change_momentum(announcements, close):
    '''
    Calculate the price momentum since the most recent earnings surprise change normalised to annualised returns
    '''

def log_returns(data):
    '''

    Parameters
    -----
    :window Pandas DataFrame

    :returns Pandas DataFrame
    '''

    assert data.index.freq == "Day"
    ret = np.log(data) - np.log(data.tshift(1))
    return ret

def index_log_returns(price):
    
    logret = log_returns(price)
    logret.dropna(how = 'all', inplace=True)
    return np.exp(logret.cumsum())*100