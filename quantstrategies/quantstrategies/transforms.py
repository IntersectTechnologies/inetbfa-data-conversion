# Copyright 2015 Intersect Technologies CC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
@author: Niel Swart
@date: 2015/06/25

transformation functions that take a dataframe as input and applies the specific transformation and returns a transformed dataframe as output.

Examples:
    Windowing functions over the data frame input

    Basic technical analysis indicators

    Data smoothing and filtering

    Sub-sampling
"""

import numpy as np
import pandas as pd

def mean(window):
    return window.mean()

def momentum(window):
    '''
    :window Pandas DataFrame

    :returns Pandas Series
    '''

    mom = np.log(window.iloc[-1]) - np.log(window.iloc[0])
    return mom

def log_returns(window):
    '''
    :window Pandas DataFrame

    :returns Pandas DataFrame
    '''

    ret = np.log(window) - np.log(window.shift(1))
    return ret

def last_mean(window, period = '1M'):
    '''
    '''

    window.fillna(method = 'pad', inplace=True)
    means = window.last(period).mean()
        
    if type(means) != pd.Series:
            raise TypeError
        
    return means

def max(window, period=50):
    return window.ix[-period:].max()

def movavg(window, period=50):
    return window.ix[-period:].mean()

def index_log_returns(window):
    window.fillna(method = 'pad', inplace=True)
    return np.exp(window.cumsum())*100

def index_price(window):
    window.fillna(method = 'pad', inplace=True)
    pct = window.pct_change()
    temp.ix[0]=100

def index_returns(window):
    window.fillna(method = 'pad', inplace=True)
    window.iloc[0] = 100
    return window.cumsum(axis=0)