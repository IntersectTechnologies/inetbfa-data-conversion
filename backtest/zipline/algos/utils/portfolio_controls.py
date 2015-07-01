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
Created on Tue Feb 10 10:31:05 2015

@author: Niel
"""

import pandas as pd

def min_max_securities(portfolio, minimum, maximum, ascending=True):
    '''
    Limit the minimum and maximum number of securities that must be held in a portfolio
    
    Parameters
    ----------
    
    portfolio :
    
    minimum :
    
    maximum :
    
    filter_func :
    
    Returns
    -------
    '''
    
    assert type(portfolio) == pd.Series
    
    portf = portfolio.sort(ascending=ascending)
    
    return portf[:maximum].index
    
def min_max_allocation(portfolio):
    '''
    
    '''