# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 12:15:04 2014

Test Algo

@author: Niel
"""
import pandas as pd
from matplotlib import pylab, pyplot
plt = pyplot
import zipline
from zipline.api import order_target, record, symbol, history, add_history, order_target_percent
from zipline.finance import trading
from zipline.utils import tradingcalendar_jse
from os import path
import sys

# Define algorithm
def initialize(context):
	'''    
	'''
	# Register 2 histories that track daily prices,
	# one with a 100 window and one with a 300 day window
	add_history(50, '1d', 'Price')
	add_history(300, '1d', 'Price')


    context.i = 0

# function to be called on each new data event
def handle_data(context, data):
	'''
	'''
	# Skip first 300 days to get full windows
	context.i += 1
	if context.i < 200:
		record(JSE_SOL=data[symbol('JSE_SOL')].Price)
		record(JSE_NPN=data[symbol('JSE_NPN')].Price)
		return
		
	# Compute averages
	# history() has to be called with the same params from above and returns a
	# pandas dataframe.
	
	mom_6m = history(125, '1d', 'Price')[-1]/history(125, '1d', 'Price')[0]
		
	short_mavg = history(50, '1d', 'Price').mean()
	long_mavg = history(200, '1d', 'Price').mean()

	# Trading logic - SOL
	if short_mavg['JSE_SOL'] > long_mavg['JSE_SOL']:
		# order_target orders as many shares as needed to
		# achieve the desired number of shares.
		order_target_percent(symbol('JSE_SOL'), 0.5)
	elif short_mavg['JSE_SOL'] < long_mavg['JSE_SOL']:
		order_target_percent(symbol('JSE_SOL'), 0.25)

	# Trading logic - NPN
	if short_mavg['JSE_NPN'] > long_mavg['JSE_NPN']:
		# order_target orders as many shares as needed to
		# achieve the desired number of shares.
		order_target_percent(symbol('JSE_NPN'), 0.5)
	elif short_mavg['JSE_NPN'] < long_mavg['JSE_NPN']:
		order_target_percent(symbol('JSE_NPN'), 0.25)
		
	# Save values for later inspection
	record(JSE_SOL=data[symbol('JSE_SOL')].Price, JSE_NPN=data[symbol('JSE_NPN')].Price)

# function to be called right after algorithm completes to analyze the performance data
def analyze(_, perf):
    '''
    '''
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	(perf.portfolio_value/100).plot(ax=ax1)
	ax1.set_ylabel('portfolio value in R')

	perf['JSE_SOL'].plot(ax=ax1)
	perf['JSE_NPN'].plot(ax=ax1)

	#    perf_trans = perf.ix[[t != [] for t in perf.transactions]]
	#    buys = perf_trans.ix[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
	#    sells = perf_trans.ix[[t[0]['amount'] < 0 for t in perf_trans.transactions]]

	#    # Markers for buy trades
	#    ax2.plot(buys.index, perf.short_mavg.ix[buys.index], '^', markersize=10, color='m')
	#    
	#    # Markers for sell trades
	#    ax2.plot(sells.index, perf.short_mavg.ix[sells.index], 'v', markersize=10, color='k')
	ax1.set_ylabel('Price in c')
	plt.legend(loc=0)
	plt.show()    

def main():
   # Algo arguments:
    start = '2006-1-1'
    end = '2013-12-31'
    source = 'quandl' 
    quandl_source = 'NIELSWART'
    authtoken = 'MBaawgy9DEZJHU3NkcNd'
    symbols = ['JSE_SOL', 'JSE_NPN']
    benchmark = 'JSE_J203'
    output = 'perf'    
    
    """
    Runs a full zipline pipeline given configuration keyword
    arguments.

    1. Load data (start and end dates can be provided a strings as
    well as the source and symobls).

    2. Instantiate algorithm (supply either algo_text or algofile
    kwargs containing initialize() and handle_data() functions). If
    algofile is supplied, will try to look for algofile_analyze.py and
    append it.

    3. Run algorithm (supply capital_base as float).

    4. Return performance dataframe.

    :Arguments:
        * print_algo : bool <default=True>
           Whether to print the algorithm to command line. Will use
           pygments syntax coloring if pygments is found.

    """
    
    # parse arguments
    start = pd.Timestamp(start, tz='UTC')
    end = pd.Timestamp(end, tz='UTC')
    symbols = symbols

    if source == 'quandl':
        source = zipline.data2.load_bars_from_quandl(source=quandl_source,
            stocks=symbols, start=start, end=end, authtoken=authtoken)    
            
    else:
        raise NotImplementedError(
            'Source %s not implemented.' % source)
												
    jse = trading.TradingEnvironment(bm_symbol=benchmark,
							exchange_tz="Africa/Johannesburg", 
							env_trading_calendar=tradingcalendar_jse,
							source=quandl_source,
							authtoken=authtoken)
                                                           
    with jse:
        algo = zipline.TradingAlgorithm(initialize=initialize, handle_data=handle_data, analyze=analyze)
        perf = algo.run(source)

    output_fname = path.join('C:\\', 'root', 'repos', 'output', output+'.csv')
    if output_fname is not None:
        perf.to_csv(output_fname)
        
    print ' Finito...'
	
if __name__ == "__main__":    
    main()
    sys.exit(0)
