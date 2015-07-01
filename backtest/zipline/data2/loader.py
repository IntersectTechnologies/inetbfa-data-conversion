#
# Copyright 2013 Quantopian, Inc.
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

import importlib
import os
from os.path import expanduser
from collections import OrderedDict
from datetime import timedelta

import logbook
import pandas as pd
import pytz
import Quandl as q

from six import iteritems

logger = logbook.Logger('Loader')

# TODO: Make this path customizable.
DATA_PATH = os.path.join(
    expanduser("~"),
    '.zipline',
    'data'
    )

CACHE_PATH = os.path.join(
    expanduser("~"),
    '.zipline',
    'cache'
    )

# Mapping from index symbol to appropriate bond data
INDEX_MAPPING = {
    '^GSPC':('treasuries', 'treasury_curves.csv', 'data.treasury.gov'),
    '^GSPTSE': ('treasuries_can', 'treasury_curves_can.csv', 'bankofcanada.ca'),
    '^FTSE':  # use US treasuries until UK bonds implemented
    ('treasuries', 'treasury_curves.csv', 'data.treasury.gov'),
    'JSE_J203': (None, 'za_tbill_91d.csv', 'NIELSWART')
}

def get_data_filepath(name):
    """
    Returns a handle to data file.
    Creates containing directory, if needed.
    """

    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    return os.path.join(DATA_PATH, name)

def get_cache_filepath(name):
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)

    return os.path.join(CACHE_PATH, name)

def get_benchmark_filename(symbol):
    return "%s_benchmark.csv" % symbol

def load_market_data(bm_symbol='JSE_J203', 
            source = 'NIELSWART',
            authtoken=None,
            start = '1990-01-01',
            end = '2013-12-31'):

    """
    Load market data from quandl

    Default to JSE - J203

    :param bm_symbol: 
    :type bm_symbol:

    """
    ################################
    # LOAD BENCHMARK DATA_PATH
    ################################

    bm_filepath = get_data_filepath(get_benchmark_filename(bm_symbol))
    try:
        saved_benchmarks = pd.Series.from_csv(bm_filepath)
    except (OSError, IOError):
        print("""Data files aren't distributed with source. Fetching data from Quandl.""")
        if source == 'GOOG' or source == 'NIELSWART':
            q_symbol = bm_symbol
        else:
            raise NotImplementedError('No other Quandl data sources have been implemented yet...')
            
        q_code = source + '/' + q_symbol
        bm_data = q.get(q_code, authtoken=authtoken, trim_start=start, trim_end=end)
        if not bm_data.empty:
            benchmark_returns = bm_data['TRI'].pct_change()
            benchmark_returns.to_csv(bm_filepath)
            saved_benchmarks = pd.Series.from_csv(bm_filepath)
        else:
            raise NotImplementedError('No data available')

    saved_benchmarks = saved_benchmarks.tz_localize('UTC')
        
    ########################################################################
    # GET RISK-FREE RATES
    ########################################################################
    # Default to SA 91 Day Treasury Bill
    module, filename, tr_source = INDEX_MAPPING.get(bm_symbol, INDEX_MAPPING[bm_symbol])

    tr_filepath = get_data_filepath(filename)
    try:
        saved_curves = pd.DataFrame.from_csv(tr_filepath)
    except (OSError, IOError):
        print("""data files aren't distributed with source. Fetching data from Quandl""")
        q_code = tr_source + '/' + 'ZA_TBILL_91D'
        tr_data = q.get(q_code, authtoken=authtoken, trim_start=start, trim_end=end)
        if not tr_data.empty:
            tr_yields = tr_data/100
            tr_yields.to_csv(tr_filepath)
            saved_curves = pd.Series.from_csv(tr_filepath)
        else:
            raise NotImplementedError('No data available')
            
    saved_curves = saved_curves.tz_localize('UTC')

    return saved_benchmarks, saved_curves
                            
def load_from_quandl(source='GOOG',
                     stocks=None,
                     start=None,
                     end=None,
                     authtoken=None, 
                     adjusted=False):
    
    """
    Loads price data from Quandl into a Pandas dataframe for each of the indicated
    securities.  

    :param stocks: Stock data to load.
    :type stocks: list

    :param start: Retrieve prices from start date on.
    :type start: datetime

    :param end: Retrieve prices until end date.
    :type end: datetime

    :param adjusted: Adjust the price for splits and dividends.
    :type adjusted: bool
    """

    assert source is not None or stocks is not None, """Must specify Quandl source and stocks"""

    if start is None:
        start = pd.datetime(1990, 1, 1, 0, 0, 0, 0, pytz.utc)

    if start is not None and end is not None:
        assert start < end, "start date is later than end date."

    tickers = []
    if stocks is not None:
        for s in stocks:
            if source == 'GOOG' or source == 'NIELSWART':
                if source == 'NIELSWART':
                    if not authtoken:
                        raise ValueError('Please give the API token')
                print 'Loading data from Quandl/' + source + '/' + s
            else:
                raise NotImplementedError('No other Quandl sources implemented yet')

            tickers.append(s)
        
        dd = OrderedDict()    # data dictionary
        
        # load for each ticker
        for ticker in tickers:
            cache_filename = "{stock}-{start}-{end}.csv".format(
                stock=ticker,
                start=start,
                end=end).replace(':', '-')
            
            cache_filepath = get_cache_filepath(cache_filename)
        
            if os.path.exists(cache_filepath):
                stkd = pd.DataFrame.from_csv(cache_filepath)
                dd[ticker] = stkd['Close']
            else:
                q_code = source + '/' + ticker
                data = q.get(q_code, trim_start = start, trim_end = end)
                data.to_csv(cache_filepath)	# save to data cache - file
                dd[ticker] = data['Close']
        
    close = pd.DataFrame(dd)
    close.fillna(method = 'pad')
    close.index = close.index.tz_localize(pytz.utc)

    return close         

def load_bars_from_quandl(source='GOOG',
                    stocks=None,
                    start=None,
                    end=None,
                    metrics = ['Open', 'High', 'Low', 'Close', 'Volume'],
                    authtoken=None,
                    adjusted=False):
    
    """
    Loads data from Quandl into a panel with the following
    column names for each indicated security:

        - Open
        - High
        - Low
        - Close
        - Volume

    :param source: Quandl data source to use - default GOOGLE FINANCE.
    :type indexes: str
    :param stocks: Stock data to load.
    :type stocks: list
    :param start: Retrieve prices from start date on.
    :type start: datetime
    :param end: Retrieve prices until end date.
    :type end: datetime
    :param metrics: The columns to load
    :type metrics: list
    :param adjusted: Adjust open/high/low/close for splits and dividends.
        The 'price' field is always adjusted.
    :type adjusted: bool

    """

    tickers = []
    for s in stocks:
        if source == 'GOOG' or source == 'NIELSWART':
            if source == 'NIELSWART':
                if not authtoken:
                    raise ValueError('Please give the API token')
            print 'Loading data from Quandl/' + source + '/' + s
        else:
            raise NotImplementedError('Only NIELSWART and GOOG Quandl sources have been implemented thus far.')
            
        tickers.append(s)

    dd = {}     # data dictionary

    # load for each ticker
    for ticker in tickers:

        cache_filename = "{stock}-{start}-{end}.csv".format(
            stock=ticker,
            start=start,
            end=end).replace(':', '-')
        
        cache_filepath = get_cache_filepath(cache_filename)

        if os.path.exists(cache_filepath):
            stkd = pd.DataFrame.from_csv(cache_filepath)
            
            # check if all the metrics are available else load data from 
            # other source
            #tf = [m is in stkd.columns for m in metrics]			
            
            dd[ticker] = stkd
        else:
            q_code = source + '/' + ticker
            data = q.get(q_code, trim_start = start, trim_end = end, authtoken=authtoken)
            data.to_csv(cache_filepath)	# save to data cache - file
            dd[ticker] = data[metrics]		
        
    panel = pd.Panel(dd)
    panel.major_axis = panel.major_axis.tz_localize(pytz.utc)
    return panel