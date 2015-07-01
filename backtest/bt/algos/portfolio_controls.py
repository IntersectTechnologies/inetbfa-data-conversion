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

import bt
from bt.core import Algo, AlgoStack
import pandas as pd
import numpy as np
import random

class LimitDeltas(Algo):

    """
    Modifies temp['weights'] based on weight delta limits.

    Basically, this can be used if we want to restrict how much a security's
    target weight can change from day to day. Useful when we want to be more
    conservative about how much we could actually trade on a given day without
    affecting the market.

    For example, if we have a strategy that is currently long 100% one
    security, and the weighing Algo sets the new weight to 0%, but we
    use this Algo with a limit of 0.1, the new target weight will
    be 90% instead of 0%.

    Args:
        * limit (float, dict): Weight delta limit. If float, this will be a
            global limit for all securities. If dict, you may specify by-ticker
            limit.

    Sets:
        * weights

    Requires:
        * weights

    """

    def __init__(self, limit=0.1):
        super(LimitDeltas, self).__init__()
        self.limit = limit
        # determine if global or specific
        self.global_limit = True
        if isinstance(limit, dict):
            self.global_limit = False

    def __call__(self, target):
        tw = target.temp['weights']
        all_keys = set(target.children.keys() + tw.keys())

        for k in all_keys:
            tgt = tw[k] if k in tw else 0.
            cur = target.children[k].weight if k in target.children else 0.
            delta = tgt - cur

            # check if we need to limit
            if self.global_limit:
                if abs(delta) > self.limit:
                    tw[k] = cur + (self.limit * np.sign(delta))
            else:
                # make sure we have a limit defined in case of limit dict
                if k in self.limit:
                    lmt = self.limit[k]
                    if abs(delta) > lmt:
                        tw[k] = cur + (lmt * np.sign(delta))

        return True


class LimitWeights(Algo):

    """
    Modifies temp['weights'] based on weight limits.

    This is an Algo wrapper around ffn's limit_weights. The purpose of this
    Algo is to limit the weight of any one specifc asset. For example, some
    Algos will set some rather extreme weights that may not be acceptable.
    Therefore, we can use this Algo to limit the extreme weights. The excess
    weight is then redistributed to the other assets, proportionally to
    their current weights.

    See ffn's limit_weights for more information.

    Args:
        * limit (float): Weight limit.

    Sets:
        * weights

    Requires:
        * weights

    """

    def __init__(self, limit=0.1):
        super(LimitWeights, self).__init__()
        self.limit = limit

    def __call__(self, target):
        if 'weights' not in target.temp:
            return True

        tw = target.temp['weights']
        tw = bt.ffn.limit_weights(tw, self.limit)
        target.temp['weights'] = tw

        return True

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