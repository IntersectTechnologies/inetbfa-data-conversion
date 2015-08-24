#...
from datamanager import load
from quantstrategies.strategies.strategy import *
from quantstrategies.transforms import mean, momentum, log_returns, index_log_returns, movavg, max
from functools import partial
from quantstrategies.universe_selection import get_all_listed, greater_than_filter, top_filter
from core.utils import getLog

log = getLog(name='Strategy')

short_movavg = partial(movavg, period=20)
long_movavg = partial(movavg, period=50)
max20 = partial(max, period = 20)

# Define Nodes
log.info('Creating data flow graph...')

def filter_universe(data, fields):
        '''
        Apply filters
        '''

        def calc_means(data, fields, period = '1M'):
    
            means = {}
            for f in fields:
                data[f].fillna(method = 'pad', inplace=True)
                means[f] = data[f].last(period).mean()
        
                if type(means[f]) != pd.Series:
                    raise TypeError
        
            return means

        means = calc_means(data, fields)
        filtered = get_all_listed()

        # Volume zero filter
        filtered = filtered.intersection(greater_than_filter(means['Volume'], 1))

        # Price filter
        filtered = filtered.intersection(greater_than_filter(data['Close'].last('1D').ix[0], 100))
    
        # Market Cap filter
        filtered = filtered.intersection(top_filter(means['Market Cap'], 200))
    
        # Trading Frequency Filter
        filtered = filtered.intersection(greater_than_filter((means['Volume']/means['Total Number Of Shares'])*100, 0.01))
    
        return(filtered)

fields = [
            'Close',
            'Market Cap',
            'Volume',
            'Total Number Of Shares',
            'VWAP'
        ]

start_date = '2014-08-01'
end_date = '2015-07-31'

# Import the last 12 month's data
data = load.load_fields(fields = fields, start = start_date, end = end_date)

filter = filter_universe(data, fields)

datan = SourceNode(data['Close'].ix[-252:])
returns = SourceNode()
reporter = SinkNode(name = 'StatsReport')

datan.filter(filter).transform(log_returns).to_(returns)
do_stats = returns.transform(index_log_returns).stats(movavg20 = short_movavg, movavg50 = long_movavg, max = max).to_(reporter)
stats = datan.stats(momentum = momentum, mean = mean).to_(reporter)

reporter.report()
datan()

do = (do_stats.data.ix['movavg20'] - do_stats.data.ix['movavg50']) / do_stats.data.ix['max']
do.to_csv('DO.csv')

log.info('Running data flow graph...')

