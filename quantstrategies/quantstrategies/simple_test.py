#...
from datamanager import load
from quantstrategies.strategies.strategy import *
from quantstrategies.transforms import mean, momentum, log_returns, index_log_returns, movavg, max
from functools import partial

from core.utils import getLog

log = getLog(name='Strategy')

short_movavg = partial(movavg, period=20)
long_movavg = partial(movavg, period=50)
max20 = partial(max, period = 20)

price_close = load.load_close()

# Define Nodes
datan = SourceNode(price_close.ix[-100:])
returns = SourceNode()
reporter = SinkNode(name = 'StatsReport')

log.info('Creating data flow graph...')

datan.filter(load.get_all_listed()).transform(log_returns).to_(returns)
do_stats = returns.transform(index_log_returns).stats(movavg20 = short_movavg, movavg50 = long_movavg, max = max).to_(reporter)
stats = datan.stats(momentum = momentum, mean = mean).to_(reporter)

reporter.report()
datan()

do = (do_stats.data.ix['movavg20'] - do_stats.data.ix['movavg50']) / do_stats.data.ix['max']
do.to_csv('DO.csv')

log.info('Running data flow graph...')

