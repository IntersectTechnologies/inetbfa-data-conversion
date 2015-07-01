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
Created on Mon Nov 10 12:15:04 2014

@author: Niel
"""

import numpy as np
from matplotlib import pyplot
plt = pyplot

from zipline.algos.utils import universe_select as us
from zipline.algos.utils import portfolio_selection as ps
from zipline.algos.utils import portfolio_controls as pc
from zipline.api import record, symbol, history, add_history, order_target_percent

NAME = 'Simple Momentum'
VERSION = (0,1,'dev')

def initialize(context):
    '''    
    '''
    # Register histories that keeps track of a moving window of data...
    add_history(250, '1d', 'Price')
    add_history(25, '1d', 'Volume')
    add_history(25, '1d', 'Total Number Of Shares')
    add_history(25, '1d', 'Number Of Trades')
    add_history(5, '1d', 'Market Cap')        

    context.i = 0

def handle_data(context, data):
    '''
    function to be called on each new data event
    '''
    
    dt = context.blotter.current_dt
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 250:
         return
         
    # Get recorded history
    # history() has to be called with the same params from above and returns a pandas dataframe.
    price = history(250, '1d', 'Price')
    volume = history(21, '1d', 'Volume')
    total_num_shares = history(21, '1d', 'Total Number Of Shares')
    numtrades = history(21, '1d', 'Number Of Trades')
    marketcap = history(5, '1d', 'Market Cap')
    
    ####
    # UNIVERSE SELECTION
    # Get the 100 most liquid stocks based on their liquidity score
    liquid_universe = us.get_most_liquid_at_date(100, dt, volume, total_num_shares, numtrades)
    filtered_price = price[liquid_universe]
    
    ####
    # SECURITY SELECTION
    # Calculate the 6 month momentum window for the filtered universe of stocks
    mom_6m = np.log(filtered_price) - np.log(filtered_price.shift(125))
    # Get the current momentum for the universe of stocks
    mom = mom_6m.ix[dt]
    
    # Select those with Momentum larger than threshold
    mom.sort(ascending=False, na_position='last')
    mom[:20].index
    
    ####
    # PORTFOLIO SELECTION
    # portfolio controls
    
    # Calculate portfolio target weights - market cap weighted
    weights = ps.value_weighted(mom[:20].index, marketcap.ix[dt])
    
    ####
    # EXECUTION
    # Trading logic
    for ticker in weights.index:
        # order_target_percent orders as many shares as needed to achieve the desired allocation
        order_target_percent(symbol(ticker), weights[ticker])
    
        # Save values for later inspection
        record(ticker=data[symbol(ticker)].Price)

# function to be called right after algorithm completes to analyze the performance data
def analyze(_, perf):
    '''
    '''

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    (perf.portfolio_value/100).plot(ax=ax1)
    ax1.set_ylabel('portfolio value in R')
    
    #    perf['JSE_SOL'].plot(ax=ax1)
    #    perf['JSE_NPN'].plot(ax=ax1)
    
    #    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
    #    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
    #    sells = perf_trans.ix[[t[0]['amount'] < 0 for t in perf_trans.transactions]]

    #    # Markers for buy trades
    #    ax2.plot(buys.index, perf.short_mavg.ix[buys.index], '^', markersize=10, color='m')
    #    
    #    # Markers for sell trades
    #    ax2.plot(sells.index, perf.short_mavg.ix[sells.index], 'v', markersize=10, color='k')
    #    ax1.set_ylabel('Price in c')
    plt.legend(loc=0)
    plt.show()    