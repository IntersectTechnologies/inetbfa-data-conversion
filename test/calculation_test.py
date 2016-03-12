from datamanager.envs import *
from datamanager.adjust import *
import pandas as pd
import datetime as dt
import numpy as np
import random
import datamanager.transforms as t
from mock_data import TESTDATA

def test_backwards_calc():
    '''
    '''

def test_adjusted_close():
    '''
    test should not be dependent on data in files
    '''
    
def test_book2market():
    '''
    '''
    
    dt_ix = [dt.date(2016, 1, d) for d in range(1,31)]
    data = data = [ random.random()*10 if (d > 15 and d < 20 or (d < 10 and d > 5)) else np.NaN for d in range(1,31)]
    
    df = pd.DataFrame(data, index = dt_ix, columns = ['Values'])
    
    df = df.ffill()

def test_surprise_sum():
    td = TESTDATA.head(10)

    assert len(td.index) == 10

    last3 = td.tail(3)
    shifted = td.shift(-2)
    sum_last3 = last3.sum()
    sum_ix = shifted.iloc[[5,6,7]].sum()

    assert sum_last3['AGL'] == sum_ix['AGL']
    
    rolsum = pd.rolling_sum(shifted, 3)

    assert np.abs(rolsum.iloc[7]['AGL'] - sum_last3['AGL']) < 0.001
    

def test_momentum():
    resampled = t.resample_monthly(TESTDATA, 'mean')

    assert isinstance(resampled, pd.DataFrame)
    assert resampled.index.freq == 'M'

    assert len(resampled.index) == 312

    # shift 12, 1
    t_mom = np.log(resampled.ix['2015-11-30']) - np.log(resampled.ix['2014-12-31'])
    mom = t.momentum_monthly(resampled, 12, 1)

    assert len(mom.index) == len(resampled.index)

    assert t_mom['AGL'] == mom.ix['2015-12-31']['AGL']
    assert t_mom['SOL'] == mom.ix['2015-12-31']['SOL']
    assert t_mom['SAB'] == mom.ix['2015-12-31']['SAB']

def test_cumulative_return():

    price = [7, 8, 9, 10, 9, 9, 8, 9, 10, 11, 10]
    index = list(range(0, 11))
    df = pd.DataFrame(price, index = index, columns = ["Data"])
    logret = np.log(df) - np.log(df.shift(1))

    pctret = df.pct_change()

