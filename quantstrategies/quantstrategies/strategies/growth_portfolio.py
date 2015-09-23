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

'''
Created on Sat May 23 15:22:03 2015
@author: Niel Swart
'''

import numpy as np
from datamanager.load import get_equities
from datamanager.envs import *
from quantstrategies.universe_selection import liquid_jse_shares

def fields():
    return [
        'Close',
        'Market Cap',
        'Volume',
        'Total Number Of Shares',
        'DY',
        'PE',
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
    mom12 = np.log(fc.shift(-21)) - np.log(fc.shift(-252))
    mom6 = np.log(fc) - np.log(fc.shift(-126))
    mom3 = np.log(fc) - np.log(fc.shift(-63))

    return (mom12, mom6, mom3)

def security_selection(data):
    '''
    Select the top 15 securities based on momentum
    '''
    
    latest_mom = data.ix[0]
    equities = get_equities()

    cols = [
    'fullname',
    'industry',
    'sector'
    ]

    output = equities[cols].ix[filtered].copy()

    output['Momentum - 12M'] = mom12.last('1D').ix[0]
    output['Momentum - 6M'] = mom6.last('1D').ix[0]
    output['Momentum - 3M'] = mom3.last('1D').ix[0]
    output['Price'] = self.data['Close'].last('1D').ix[0]
    output['DY'] = self.data['DY'][filtered].last('1D').ix[0]
    output['PE'] = self.data['PE'][filtered].last('1D').ix[0]

    # RANK
    return(output.sort(columns = 'Momentum - 6M', ascending = False))

def portfolio_selection(data):
    '''
    '''
