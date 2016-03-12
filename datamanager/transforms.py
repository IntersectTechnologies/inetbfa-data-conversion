'''
This module contains transformation functions for time series data based on pandas DataFrame's
'''

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
    mom = np.log(close.tshift(end_lag)) - np.log(close.tshift(start_lag))

    return mom
    
def earnings_momentum(ey, close, start_lag, end_lag):
    '''
    Calculate the momentum in the fundamental earnings of the company derived from the EY and the closing price
    '''
    
def pead_momentum(announcements, close):
    '''
    Calculate the price momentum from the most recent earnings annoucnement normalised to annualised returns
    A minimum of 2 days since the announcement (from day 3) is required. 
    
    Parameters
    -----------
    
    
    Rerturns
    -----------
    
    '''

def earnings_surprise(announcements, close):
    '''
    Calculate the earnings surprise defined as the the cumulative return after a company earnings announcement for the days 0-2
    
    Returns
    -----
    surprise : pandas.DataFrame
        The cumulative return (surprise) values on the announcement days (index) - all NaN rows removed
    '''

def earnings_surprise_changes(announcements, close):
    '''
    Calculates the change in earnings suprises by comparing an earnings surprise to a previous surprise
    '''    

def earnings_surprise_change_momentum(announcements, close):
    '''
    Calculate the price momentum since the most recent earnings surprise change normalised to annualised returns
    '''

def log_returns(data):
    '''
    :window Pandas DataFrame

    :returns Pandas DataFrame
    '''

    assert data.freq == 'D'
    ret = np.log(data) - np.log(data.tshift(1))
    return ret