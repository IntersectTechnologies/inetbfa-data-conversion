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

transforms = {
    'mean' : mean,
    'momentum': momentum,    
}

def mean(window):

    window.mean()


def momentum(window):
    '''
    '''

    mom = np.log(window.end) - np.log(window.start)

def last_mean(data, period = '1M'):
    '''
    '''

    data.fillna(method = 'pad', inplace=True)
    means = data.last(period).mean()
        
    if type(means) != pd.Series:
            raise TypeError
        
    return means